from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()


class Author(db.Model):
    """Guest author / contributor profile (distinct from Admin login)."""
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    slug        = db.Column(db.String(120), unique=True, nullable=False)
    bio         = db.Column(db.Text, nullable=True)
    avatar      = db.Column(db.String(500), nullable=True)  # Cloudinary URL
    email       = db.Column(db.String(150), nullable=True)
    twitter     = db.Column(db.String(100), nullable=True)  # handle only
    posts       = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<Author {self.name}>'


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
    image = db.Column(db.String(500), nullable=True)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read_time = db.Column(db.String(20), default='5 min read')
    status = db.Column(db.String(20), default='draft')  # 'draft', 'published', 'scheduled'
    scheduled_for = db.Column(db.DateTime, nullable=True)  # auto-publish at this UTC time
    is_featured = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(200), nullable=True)  # comma-separated tags
    view_count  = db.Column(db.Integer, default=0, nullable=False)
    author_id   = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)  # None = site owner
    comments = db.relationship('Comment', backref='post', lazy=True)

    def is_published(self):
        return self.status == 'published'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    approved = db.Column(db.Boolean, default=False, nullable=False)  # requires admin approval


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    date_subscribed = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

class PodcastEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    episode_number = db.Column(db.Integer, nullable=True)
    audio_url = db.Column(db.String(500), nullable=True)       # Cloudinary hosted audio
    spotify_url = db.Column(db.String(500), nullable=True)     # optional Spotify embed
    cover_image = db.Column(db.String(500), nullable=True)
    duration = db.Column(db.String(20), nullable=True)         # e.g. "34 min"
    date_published = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='published')     # published / draft



class PostSeries(db.Model):
    """Groups posts into a named series with ordering."""
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    slug        = db.Column(db.String(220), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    entries     = db.relationship('PostSeriesEntry', backref='series',
                                  order_by='PostSeriesEntry.position', lazy=True)


class PostSeriesEntry(db.Model):
    """Maps a Post to a PostSeries with a position index."""
    id        = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('post_series.id'), nullable=False)
    post_id   = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    position  = db.Column(db.Integer, nullable=False, default=1)
    post      = db.relationship('Post', backref=db.backref('series_entries', lazy=True))
