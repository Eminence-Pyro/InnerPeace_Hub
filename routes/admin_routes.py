from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import uuid
import cloudinary
import cloudinary.uploader
from flask_login import login_required
from slugify import slugify
from models import Post, Message, db
from utils import allowed_file, generate_slug

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    messages = Message.query.order_by(Message.date_sent.desc()).all()
    unread = Message.query.filter_by(is_read=False).count()
    published = Post.query.filter_by(status='published').count()
    drafts = Post.query.filter_by(status='draft').count()

    return render_template(
        'admin/dashboard.html',
        posts=posts,
        messages=messages,
        unread=unread,
        published=published,
        drafts=drafts
    )


@admin_bp.route('/admin/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        read_time = request.form.get('read_time')
        status = request.form.get('status', 'draft')  # draft or published
        is_featured = request.form.get('is_featured') == 'on'
        tags = request.form.get('tags', '')
        image_file = request.files.get('image')

        if not title or not category or not content:
            flash("Title, category and content are required")
            return redirect(url_for('admin.create_post'))

        slug = generate_slug(title)

        # Ensure unique slug
        existing = Post.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"

        image_filename = None

        if image_file and allowed_file(image_file.filename):
            upload_result = cloudinary.uploader.upload(image_file)
            image_filename = upload_result['secure_url']

        new_post = Post(
            title=title,
            slug=slug,
            category=category,
            excerpt=excerpt,
            content=content,
            read_time=read_time,
            status=status,
            is_featured=is_featured,
            tags=tags,
            image=image_filename
        )

        db.session.add(new_post)
        db.session.commit()

        flash(f"Post saved as {status}")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/create_post.html')


@admin_bp.route('/upload', methods=['POST'])
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

    try:
        upload_result = cloudinary.uploader.upload(file)

        return jsonify({
            "uploaded": True,
            "url": upload_result['secure_url']
        })

    except Exception as e:
        return jsonify({
            "uploaded": False,
            "error": {"message": str(e)}
        })


@admin_bp.route('/admin/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = generate_slug(post.title)
        post.category = request.form.get('category')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.read_time = request.form.get('read_time')
        post.status = request.form.get('status', 'draft')
        post.is_featured = request.form.get('is_featured') == 'on'
        post.tags = request.form.get('tags', '')

        image_file = request.files.get('image')

        if image_file and allowed_file(image_file.filename):
            upload_result = cloudinary.uploader.upload(image_file)
            post.image = upload_result['secure_url']

        db.session.commit()
        flash(f"Post updated and saved as {post.status}")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/create_post.html', post=post)


@admin_bp.route('/admin/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{title}' deleted successfully")
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/admin/message/<int:message_id>')
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
