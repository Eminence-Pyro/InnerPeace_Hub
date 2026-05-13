from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from models import Post, Message, db
from utils import generate_slug

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    posts = Post.query.filter_by(status='published').order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', posts=posts)


@blog_bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    
    query = Post.query.filter_by(status='published')
    
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
        # Admins can preview any post including drafts
        post = Post.query.filter_by(slug=slug).first_or_404()
    else:
        # Public only sees published posts
        post = Post.query.filter_by(slug=slug, status='published').first_or_404()

    related = Post.query.filter(
        Post.category == post.category,
        Post.id != post.id,
        Post.status == 'published'
    ).limit(2).all()
    return render_template('post.html', post=post, related=related)


@blog_bp.route('/about')
def about():
    return render_template('about.html')


@blog_bp.route('/podcast')
def podcast():
    return render_template('podcast.html')


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
