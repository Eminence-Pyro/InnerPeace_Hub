from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import cloudinary

from config import Config
from models import db, Admin
from routes.blog_routes import blog_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp


def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CKEditor(app)
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
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

    # Initialize database and create admin user
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

    return app


# Create the app instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)