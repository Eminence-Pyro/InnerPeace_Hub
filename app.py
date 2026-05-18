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
        from flask_migrate import upgrade as db_upgrade, stamp as db_stamp
        from sqlalchemy import inspect, text

        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            # Brand-new database: run all migrations from scratch
            db_upgrade()

        elif 'alembic_version' not in existing_tables:
            # Tables exist (created by old db.create_all) but no migration history.
            # Add missing columns manually then stamp as up-to-date so migrate doesn't re-run.
            with db.engine.connect() as conn:
                col_map = {col['name'] for col in inspector.get_columns('post')}
                if 'view_count' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0"))
                    print("[DB] Added post.view_count")
                if 'scheduled_for' not in col_map:
                    conn.execute(text("ALTER TABLE post ADD COLUMN scheduled_for DATETIME"))
                    print("[DB] Added post.scheduled_for")
                comment_cols = {col['name'] for col in inspector.get_columns('comment')}
                if 'approved' not in comment_cols:
                    conn.execute(text("ALTER TABLE comment ADD COLUMN approved BOOLEAN NOT NULL DEFAULT 0"))
                    print("[DB] Added comment.approved")
                conn.commit()
            db_stamp('head')   # mark all migrations as applied
            print("[DB] Stamped migration head on existing schema.")

        else:
            # Normal case: db exists with migration history — just apply pending ones
            db_upgrade()

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
