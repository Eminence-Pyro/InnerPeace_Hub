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

    related = Post.query.filter(
        Post.category == post.category,
        Post.id != post.id,
        Post.status == 'published'
    ).limit(2).all()

    # Only show approved comments publicly
    approved_comments = Comment.query.filter_by(
        post_id=post.id, approved=True
    ).order_by(Comment.date_posted.asc()).all()

    return render_template('post.html', post=post, related=related, comments=approved_comments)


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

