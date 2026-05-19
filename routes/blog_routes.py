import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from models import Post, Message, Subscriber, PodcastEpisode, Comment, db
from utils import generate_slug

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    from datetime import datetime, timezone as tz
    now = datetime.now(tz.utc)
    posts = Post.query.filter(
        db.or_(
            Post.status == 'published',
            db.and_(Post.status == 'scheduled', Post.scheduled_for <= now)
        )
    ).order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', posts=posts)


@blog_bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    from datetime import datetime, timezone as tz
    now = datetime.now(tz.utc)
    query = Post.query.filter(
        db.or_(
            Post.status == 'published',
            db.and_(Post.status == 'scheduled', Post.scheduled_for <= now)
        )
    )
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            (Post.title.ilike(f'%{search}%')) |
            (Post.excerpt.ilike(f'%{search}%')) |
            (Post.tags.ilike(f'%{search}%'))
        )
    
    posts = query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    categories = db.session.query(Post.category).filter_by(status='published').distinct().all()
    
    return render_template('blog.html', posts=posts, categories=categories, current_category=category, search=search)


@blog_bp.route('/post/<slug>')
def post(slug):
    if current_user.is_authenticated:
        post = Post.query.filter_by(slug=slug).first_or_404()
    else:
        post = Post.query.filter_by(slug=slug, status='published').first_or_404()

    # ── View counter — increment on each visit, skip admin previews ────────────
    if not current_user.is_authenticated:
        try:
            post.view_count = (post.view_count or 0) + 1
            db.session.commit()
        except Exception:
            db.session.rollback()

    # ── Improvement 6: Related posts via tag + category similarity ──────────────
    related = []
    if post.tags:
        tag_list = [t.strip() for t in post.tags.split(',') if t.strip()]
        # Score each candidate post by how many tags it shares
        candidates = Post.query.filter(
            Post.status == 'published',
            Post.id != post.id,
            Post.category == post.category
        ).all()
        scored = []
        for c in candidates:
            c_tags = set(t.strip() for t in (c.tags or '').split(',') if t.strip())
            score = len(set(tag_list) & c_tags)
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        related = [c for _, c in scored[:3]]

    # Fall back to same-category if no tag matches
    if not related:
        related = Post.query.filter(
            Post.category == post.category,
            Post.id != post.id,
            Post.status == 'published'
        ).limit(3).all()

    # Only show approved comments publicly
    approved_comments = Comment.query.filter_by(
        post_id=post.id, approved=True
    ).order_by(Comment.date_posted.asc()).all()

    # ── Improvement 11: Series prev/next navigation ──────────────────────────
    series_data = None
    if post.series_entries:
        entry = post.series_entries[0]
        series = entry.series
        positions = [e.post_id for e in series.entries]
        current_pos = entry.position
        prev_post = None
        next_post = None
        for e in series.entries:
            if e.position == current_pos - 1:
                prev_post = e.post
            if e.position == current_pos + 1:
                next_post = e.post
        series_data = {
            'series': series,
            'position': current_pos,
            'total': len(positions),
            'prev': prev_post,
            'next': next_post,
        }

    return render_template('post.html', post=post, related=related,
                           comments=approved_comments, series_data=series_data)


@blog_bp.route('/about')
def about():
    return render_template('about.html')


@blog_bp.route('/podcast')
def podcast():
    episodes = PodcastEpisode.query.filter_by(status='published').order_by(PodcastEpisode.date_published.desc()).all()
    return render_template('podcast.html', episodes=episodes)


@blog_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not subject or not message:
            flash("All fields are required")
            return redirect(url_for('blog.contact'))

        new_message = Message(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Message sent successfully")
        return redirect(url_for('blog.contact'))

    return render_template('contact.html')

@blog_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    name = request.form.get('name', '').strip()

    if not email or '@' not in email:
        flash('Please enter a valid email address.')
        return redirect(request.referrer or url_for('blog.index'))

    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.session.commit()
            flash("Welcome back! You've been re-subscribed.")
        else:
            flash("You're already subscribed — thank you!")
        return redirect(request.referrer or url_for('blog.index'))

    subscriber = Subscriber(email=email, name=name)
    db.session.add(subscriber)
    db.session.commit()
    flash("You're subscribed! Welcome to the InnerPeace Hub community 🎉")
    return redirect(request.referrer or url_for('blog.index'))

@blog_bp.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    body = request.form.get('body', '').strip()

    if not name or not email or not body:
        flash('All comment fields are required.')
        return redirect(url_for('blog.post', slug=slug) + '#comments')

    comment = Comment(post_id=post.id, name=name, email=email, body=body, approved=False)
    db.session.add(comment)
    db.session.commit()
    flash('Thanks! Your comment is awaiting moderation and will appear shortly. 🙏')
    return redirect(url_for('blog.post', slug=slug) + '#comments')

# ── Improvement 5: Dedicated search results page ─────────────────────────────
@blog_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        results = Post.query.filter(
            Post.status == 'published',
            db.or_(
                Post.title.ilike('%' + q + '%'),
                Post.excerpt.ilike('%' + q + '%'),
                Post.tags.ilike('%' + q + '%'),
                Post.category.ilike('%' + q + '%'),
                Post.content.ilike('%' + q + '%'),
            )
        ).order_by(Post.date_posted.desc()).all()
    return render_template('search.html', query=q, results=results)


# ── Improvement 8: RSS Feed ──────────────────────────────────────────────────
@blog_bp.route('/rss.xml')
def rss_feed():
    import html as html_mod
    from flask import Response
    posts = Post.query.filter_by(status='published').order_by(Post.date_posted.desc()).limit(20).all()
    site_url = os.environ.get('SITE_URL', 'https://innerpeacehub.onrender.com')
    items = ''
    for p in posts:
        pub_date = p.date_posted.strftime('%a, %d %b %Y %H:%M:%S +0000') if p.date_posted else ''
        excerpt = html_mod.escape(p.excerpt or '')
        title   = html_mod.escape(p.title)
        cat     = html_mod.escape(p.category or '')
        items += (
            '<item>'
            '<title>' + title + '</title>'
            '<link>' + site_url + '/post/' + p.slug + '</link>'
            '<guid isPermaLink="true">' + site_url + '/post/' + p.slug + '</guid>'
            '<description>' + excerpt + '</description>'
            '<category>' + cat + '</category>'
            '<pubDate>' + pub_date + '</pubDate>'
            '</item>'
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">'
        '<channel>'
        '<title>InnerPeace Hub</title>'
        '<link>' + site_url + '</link>'
        '<description>Healing, faith, and personal growth</description>'
        '<language>en-us</language>'
        '<atom:link href="' + site_url + '/rss.xml" rel="self" type="application/rss+xml"/>'
        + items +
        '</channel></rss>'
    )
    return Response(rss, mimetype='application/rss+xml')


# ── Improvement 9: Sitemap ───────────────────────────────────────────────────
@blog_bp.route('/sitemap.xml')
def sitemap():
    from datetime import datetime
    from flask import Response
    site_url = os.environ.get('SITE_URL', 'https://innerpeacehub.onrender.com')
    posts = Post.query.filter_by(status='published').order_by(Post.date_posted.desc()).all()
    today = datetime.utcnow().strftime('%Y-%m-%d')
    static_pages = [
        ('/', '1.0', 'weekly'),
        ('/blog', '0.9', 'daily'),
        ('/podcast', '0.8', 'weekly'),
        ('/about', '0.6', 'monthly'),
        ('/contact', '0.5', 'monthly'),
        ('/search', '0.5', 'monthly'),
    ]
    urls = ''
    for path, priority, freq in static_pages:
        urls += (
            '<url>'
            '<loc>' + site_url + path + '</loc>'
            '<lastmod>' + today + '</lastmod>'
            '<changefreq>' + freq + '</changefreq>'
            '<priority>' + priority + '</priority>'
            '</url>'
        )
    for p in posts:
        lastmod = p.date_posted.strftime('%Y-%m-%d') if p.date_posted else today
        urls += (
            '<url>'
            '<loc>' + site_url + '/post/' + p.slug + '</loc>'
            '<lastmod>' + lastmod + '</lastmod>'
            '<changefreq>monthly</changefreq>'
            '<priority>0.7</priority>'
            '</url>'
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls +
        '</urlset>'
    )
    return Response(xml, mimetype='application/xml')

# ── Improvement 12: PWA offline fallback page ────────────────────────────────
@blog_bp.route('/offline')
def offline():
    return render_template('offline.html')

# ── PWA: serve sw.js from root for correct scope ─────────────────────────────
@blog_bp.route('/sw.js')
def service_worker():
    from flask import send_from_directory, make_response
    import os as _os
    response = make_response(
        send_from_directory(_os.path.join(blog_bp.root_path, '..', 'static'), 'sw.js')
    )
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Cache-Control'] = 'no-cache'
    return response

# ── Google Search Console verification ───────────────────────────────────────
@blog_bp.route('/google5bc2898caf6741a.html')
def google_verify():
    from flask import send_from_directory
    import os as _os
    return send_from_directory(
        _os.path.join(blog_bp.root_path, '..', 'static'),
        'google5bc2898caf6741a.html'
    )
