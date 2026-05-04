from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask import jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import uuid
from slugify import slugify
import re


app = Flask(__name__)

# ===== CONFIG =====
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_ENABLE_CSRF'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB upload limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

# ===== HELPERS =====

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    return slug

# ===== MODELS =====

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    excerpt = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    read_time = db.Column(db.String(20), default='5 min read')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ===== PUBLIC ROUTES =====

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', posts=posts)

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('blog.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    related = Post.query.filter(
        Post.category == post.category,
        Post.id != post.id
    ).limit(2).all()
    return render_template('post.html', post=post, related=related)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/podcast')
def podcast():
    return render_template('podcast.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not subject or not message:
            flash("All fields are required")
            return redirect(url_for('contact'))

        new_message = Message(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Message sent successfully")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# ===== ADMIN ROUTES =====

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))

        flash('Invalid username or password')

    return render_template('admin/login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    messages = Message.query.order_by(Message.date_sent.desc()).all()
    unread = Message.query.filter_by(is_read=False).count()

    return render_template(
        'admin/dashboard.html',
        posts=posts,
        messages=messages,
        unread=unread
    )

@app.route('/admin/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = slugify(title)
        category = request.form.get('category')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')  # CKEditor will still submit via form
        read_time = request.form.get('read_time')
        image_file = request.files.get('image')

        if not title or not category or not content:
            flash("Title, category and content are required")
            return redirect(url_for('create_post'))

        slug = generate_slug(title)

        # Ensure unique slug
        existing = Post.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"

        image_filename = None

        if image_file and allowed_file(image_file.filename):
            ext = image_file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        new_post = Post(
            title=title,
            slug=slug,
            category=category,
            excerpt=excerpt,
            content=content,
            read_time=read_time,
            image=image_filename
        )

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/create_post.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('upload')

    if not file or file.filename == '':
        return jsonify({
            "uploaded": False,
            "error": {"message": "No file uploaded"}
        })

    if not allowed_file(file.filename):
        return jsonify({
            "uploaded": False,
            "error": {"message": "Invalid file type"}
        })

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    file_url = url_for('static', filename=f'images/{filename}')

    return jsonify({
        "uploaded": True,
        "url": file_url
    })
    
@app.route('/admin/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = slugify(post.title)
        post.category = request.form.get('category')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.read_time = request.form.get('read_time')

        image_file = request.files.get('image')

        if image_file and allowed_file(image_file.filename):
            ext = image_file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.image = filename

        db.session.commit()
        flash("Post updated successfully")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/create_post.html', post=post)

@app.route('/admin/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()

    return render_template(
        'admin/dashboard.html',
        selected_message=message,
        posts=Post.query.all(),
        messages=Message.query.order_by(Message.date_sent.desc()).all(),
        unread=Message.query.filter_by(is_read=False).count()
    )

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# ===== INIT DB =====

def init_db():
    with app.app_context():
        db.create_all()

        if not Admin.query.first():
            admin = Admin(
                username='ezinne',
                password=generate_password_hash('innerpeace2026')
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin created: username=ezinne password=innerpeace2026')

# ===== RUN =====

if __name__ == '__main__':
    init_db()
    app.run(debug=True)