from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import uuid
import cloudinary
import cloudinary.uploader
from flask_login import login_required
from slugify import slugify
from models import Subscriber, Post, Message, PodcastEpisode, db
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

        if image_file and image_file.filename and allowed_file(image_file.filename):
            try:
                upload_result = cloudinary.uploader.upload(image_file)
                image_filename = upload_result['secure_url']
            except Exception as e:
                flash(f'Image upload failed: {str(e)}. Try a smaller image.')
                return redirect(url_for('admin.create_post'))

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
        new_title = request.form.get('title', '').strip()
        if not new_title:
            flash('Title is required.')
            return redirect(url_for('admin.edit_post', post_id=post.id))

        # Only regenerate slug if title actually changed
        if new_title != post.title:
            new_slug = generate_slug(new_title)
            # Ensure slug uniqueness (skip self)
            existing = Post.query.filter(Post.slug == new_slug, Post.id != post.id).first()
            if existing:
                new_slug = f"{new_slug}-{uuid.uuid4().hex[:6]}"
            post.slug = new_slug

        post.title    = new_title
        post.category = request.form.get('category')
        post.excerpt  = request.form.get('excerpt')
        post.content  = request.form.get('content')
        post.read_time = request.form.get('read_time')
        post.status   = request.form.get('status', 'draft')
        post.is_featured = request.form.get('is_featured') == 'on'
        post.tags     = request.form.get('tags', '')

        image_file = request.files.get('image')
        if image_file and image_file.filename and allowed_file(image_file.filename):
            try:
                upload_result = cloudinary.uploader.upload(image_file)
                post.image = upload_result['secure_url']
            except Exception as e:
                flash(f'Image upload failed: {str(e)}')
                return redirect(url_for('admin.edit_post', post_id=post.id))

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

@admin_bp.route('/subscribers')
@login_required
def subscribers():
    subs = Subscriber.query.order_by(Subscriber.date_subscribed.desc()).all()
    return render_template('admin/subscribers.html', subscribers=subs)

# ─── Podcast Episodes ──────────────────────────────────────

@admin_bp.route('/admin/podcast')
@login_required
def podcast_list():
    episodes = PodcastEpisode.query.order_by(PodcastEpisode.date_published.desc()).all()
    return render_template('admin/podcast_list.html', episodes=episodes)


@admin_bp.route('/admin/podcast/create', methods=['GET', 'POST'])
@login_required
def create_episode():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        episode_number = request.form.get('episode_number') or None
        spotify_url = request.form.get('spotify_url', '').strip()
        duration = request.form.get('duration', '').strip()
        status = request.form.get('status', 'published')
        audio_file = request.files.get('audio_file')
        cover_file = request.files.get('cover_image')

        if not title:
            flash('Episode title is required.')
            return redirect(url_for('admin.create_episode'))

        # Check for direct browser upload URL first (bypasses Flask size limit)
        audio_url = request.form.get('audio_url_direct', '').strip() or None

        # Fall back to server-side upload if a file was submitted the traditional way
        if audio_file and audio_file.filename and not audio_url:
            try:
                result = cloudinary.uploader.upload(
                    audio_file,
                    resource_type='video',
                    folder='innerpeacehub/podcasts'
                )
                audio_url = result['secure_url']
            except Exception as e:
                flash(f'Audio upload failed: {str(e)}')
                return redirect(url_for('admin.create_episode'))

        cover_url = None
        if cover_file and allowed_file(cover_file.filename):
            result = cloudinary.uploader.upload(cover_file, folder='innerpeacehub/podcast_covers')
            cover_url = result['secure_url']

        episode = PodcastEpisode(
            title=title,
            description=description,
            episode_number=int(episode_number) if episode_number else None,
            audio_url=audio_url,
            spotify_url=spotify_url or None,
            cover_image=cover_url,
            duration=duration or None,
            status=status
        )
        db.session.add(episode)
        db.session.commit()
        flash(f"Episode '{title}' saved.")
        return redirect(url_for('admin.podcast_list'))

    return render_template('admin/create_episode.html')


@admin_bp.route('/admin/podcast/edit/<int:episode_id>', methods=['GET', 'POST'])
@login_required
def edit_episode(episode_id):
    episode = PodcastEpisode.query.get_or_404(episode_id)

    if request.method == 'POST':
        episode.title = request.form.get('title', '').strip()
        episode.description = request.form.get('description', '').strip()
        ep_num = request.form.get('episode_number')
        episode.episode_number = int(ep_num) if ep_num else None
        episode.spotify_url = request.form.get('spotify_url', '').strip() or None
        episode.duration = request.form.get('duration', '').strip() or None
        episode.status = request.form.get('status', 'published')

        # Check for direct browser upload URL
        direct_audio_url = request.form.get('audio_url_direct', '').strip()
        if direct_audio_url:
            episode.audio_url = direct_audio_url

        # Fall back to server-side upload
        audio_file = request.files.get('audio_file')
        if audio_file and audio_file.filename and not direct_audio_url:
            try:
                result = cloudinary.uploader.upload(
                    audio_file,
                    resource_type='video',
                    folder='innerpeacehub/podcasts'
                )
                episode.audio_url = result['secure_url']
            except Exception as e:
                flash(f'Audio upload failed: {str(e)}')
                return redirect(url_for('admin.edit_episode', episode_id=episode.id))

        cover_file = request.files.get('cover_image')
        if cover_file and allowed_file(cover_file.filename):
            result = cloudinary.uploader.upload(cover_file, folder='innerpeacehub/podcast_covers')
            episode.cover_image = result['secure_url']

        db.session.commit()
        flash('Episode updated.')
        return redirect(url_for('admin.podcast_list'))

    return render_template('admin/create_episode.html', episode=episode)


@admin_bp.route('/admin/podcast/delete/<int:episode_id>', methods=['POST'])
@login_required
def delete_episode(episode_id):
    episode = PodcastEpisode.query.get_or_404(episode_id)
    db.session.delete(episode)
    db.session.commit()
    flash('Episode deleted.')
    return redirect(url_for('admin.podcast_list'))

