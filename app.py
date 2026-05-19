import os
from flask import Flask, render_template
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import cloudinary

from config import ProductionConfig, DevelopmentConfig

# ── Improvement 13: Sentry error monitoring ───────────────────────────────────
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
            traces_sample_rate=0.1,   # 10% of requests traced for performance
            send_default_pii=False,   # never send passwords or personal data
            environment=os.environ.get('FLASK_ENV', 'development'),
        )
        print('[Sentry] Initialized.')
    except ImportError:
        print('[Sentry] sentry-sdk not installed. Run: pip install sentry-sdk')

config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig

from models import db, Admin
from routes.blog_routes import blog_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp


def create_app(config_class=config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CKEditor(app)
    Migrate(app, db)

    # CSRF Protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Configure Cloudinary
    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET')
    )

    # Configure login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.admin_login'

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Initialize database — run all pending migrations then seed admin
    with app.app_context():
        from flask_migrate import upgrade as db_upgrade
        from sqlalchemy import inspect, text

        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            # Brand-new database: run all migrations from scratch
            db_upgrade()

        elif 'alembic_version' not in existing_tables:
            # Tables exist but no migration history — patch columns + create new tables + stamp
            with db.engine.connect() as conn:
                all_tables = set(inspector.get_table_names())

                # post columns
                col_map = {col['name'] for col in inspector.get_columns('post')}
                if 'view_count' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0"))
                    print("[DB] Added post.view_count")
                if 'scheduled_for' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN scheduled_for DATETIME"))
                    print("[DB] Added post.scheduled_for")
                if 'is_featured' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN is_featured BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added post.is_featured")
                if 'tags' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN tags VARCHAR(300)"))
                    print("[DB] Added post.tags")

                # comment columns
                comment_cols = {col['name'] for col in inspector.get_columns('comment')}
                if 'approved' not in comment_cols:
                    conn.execute(text("ALTER TABLE comment ADD COLUMN approved BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added comment.approved")
                if 'is_admin' not in comment_cols:
                    conn.execute(text("ALTER TABLE comment ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added comment.is_admin")
# already present

                # admin columns
                admin_cols = {col['name'] for col in inspector.get_columns('admin')}
                if 'totp_secret' not in admin_cols:
                    conn.execute(text("ALTER TABLE admin ADD COLUMN totp_secret VARCHAR(32)"))
                    print("[DB] Added admin.totp_secret")
                if 'totp_enabled' not in admin_cols:
                    conn.execute(text("ALTER TABLE admin ADD COLUMN totp_enabled BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added admin.totp_enabled")

                # author table
                if 'author' not in all_tables:
                    sql = ("CREATE TABLE author ("
                           "id SERIAL PRIMARY KEY,"
                           "name VARCHAR(100) NOT NULL,"
                           "slug VARCHAR(120) NOT NULL UNIQUE,"
                           "bio TEXT,"
                           "avatar VARCHAR(500),"
                           "email VARCHAR(150),"
                           "twitter VARCHAR(100))")
                    conn.execute(text(sql))
                    print("[DB] Created author table")

                # author_id on post
                col_map2 = {col['name'] for col in inspector.get_columns('post')}
                if 'author_id' not in col_map2:
                    conn.execute(text("ALTER TABLE post ADD COLUMN author_id INTEGER REFERENCES author(id)"))
                    print("[DB] Added post.author_id")

                # post_series table
                if 'post_series' not in all_tables:
                    sql2 = ("CREATE TABLE post_series ("
                            "id SERIAL PRIMARY KEY,"
                            "title VARCHAR(200) NOT NULL,"
                            "slug VARCHAR(220) NOT NULL UNIQUE,"
                            "description TEXT,"
                            "created_at DATETIME)")
                    conn.execute(text(sql2))
                    print("[DB] Created post_series table")

                # post_series_entry table
                if 'post_series_entry' not in all_tables:
                    sql3 = ("CREATE TABLE post_series_entry ("
                            "id SERIAL PRIMARY KEY,"
                            "series_id INTEGER NOT NULL REFERENCES post_series(id),"
                            "post_id INTEGER NOT NULL REFERENCES post(id),"
                            "position INTEGER NOT NULL DEFAULT 1)")
                    conn.execute(text(sql3))
                    print("[DB] Created post_series_entry table")

                # stamp at latest head
                conn.execute(text("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))"))
                conn.execute(text("DELETE FROM alembic_version"))
                conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('c3d4e5f6a7b8')"))
                conn.commit()
            print("[DB] Schema patched and stamped at head.")

        else:
            # Normal case: db exists with migration history — just apply pending ones
            db_upgrade()
            # Safety net: ensure new tables exist even if migration was already stamped
            with db.engine.connect() as conn:
                tables = set(inspector.get_table_names())
                if 'author' not in tables:
                    sql = ("CREATE TABLE IF NOT EXISTS author (id SERIAL PRIMARY KEY,"
                           "name VARCHAR(100) NOT NULL,slug VARCHAR(120) NOT NULL UNIQUE,"
                           "bio TEXT,avatar VARCHAR(500),email VARCHAR(150),twitter VARCHAR(100))")
                    conn.execute(text(sql))
                    print("[DB] Created missing author table")
                if 'post_series' not in tables:
                    conn.execute(text("CREATE TABLE IF NOT EXISTS post_series (id SERIAL PRIMARY KEY,title VARCHAR(200) NOT NULL,slug VARCHAR(220) NOT NULL UNIQUE,description TEXT,created_at DATETIME)"))
                    print("[DB] Created missing post_series table")
                if 'post_series_entry' not in tables:
                    conn.execute(text("CREATE TABLE IF NOT EXISTS post_series_entry (id SERIAL PRIMARY KEY,series_id INTEGER NOT NULL REFERENCES post_series(id),post_id INTEGER NOT NULL REFERENCES post(id),position INTEGER NOT NULL DEFAULT 1)"))
                    print("[DB] Created missing post_series_entry table")
                admin_cols = {col['name'] for col in inspector.get_columns('admin')}
                if 'totp_secret' not in admin_cols:
                    conn.execute(text("ALTER TABLE admin ADD COLUMN totp_secret VARCHAR(32)"))
                    print("[DB] Added admin.totp_secret")
                if 'totp_enabled' not in admin_cols:
                    conn.execute(text("ALTER TABLE admin ADD COLUMN totp_enabled BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added admin.totp_enabled")
                conn.commit()

        if not Admin.query.first():
            admin = Admin(
                username='ezinne',
                password=generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'changeme'))
            )
            db.session.add(admin)
            db.session.commit()
            print('Default admin created. Set ADMIN_PASSWORD in your .env file.')



    @app.errorhandler(413)
    def file_too_large(e):
        from flask import request, redirect, url_for, flash
        flash('The file you uploaded is too large. Please compress it and try again.')
        return redirect(request.referrer or url_for('admin.admin_dashboard'))

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/404.html'), 400

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        # Roll back any broken DB transaction so the next request starts clean
        try:
            db.session.rollback()
        except Exception:
            pass
        return render_template('errors/500.html'), 500

    return app


# Create the app instance
app = create_app()


if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug)
