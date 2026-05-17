import os
from flask import Flask, render_template
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import cloudinary

from config import ProductionConfig, DevelopmentConfig

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

    # Initialize database and seed default admin
    with app.app_context():
        db.create_all()

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
        return render_template('errors/500.html'), 500

    return app


# Create the app instance
app = create_app()


if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug)
