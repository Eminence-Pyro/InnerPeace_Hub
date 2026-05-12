from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
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

    # CSRF Protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Temporary exemptions for standard HTML forms
    csrf.exempt(auth_bp)
    csrf.exempt(admin_bp)
    csrf.exempt(blog_bp)
    
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

    # Initialize database and create admin user
    with app.app_context():
        db.create_all()
        
        # Handle schema migrations for existing databases
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            # Check if Post table exists and has the new columns
            if 'post' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('post')]
                
                # Add missing columns if they don't exist
                with db.engine.begin() as conn:
                    if 'status' not in columns:
                        conn.execute(text("ALTER TABLE post ADD COLUMN status VARCHAR(20) DEFAULT 'draft'"))
                        print('Added status column to post table')
                    
                    if 'is_featured' not in columns:
                        conn.execute(text("ALTER TABLE post ADD COLUMN is_featured BOOLEAN DEFAULT FALSE"))
                        print('Added is_featured column to post table')
                    
                    if 'tags' not in columns:
                        conn.execute(text("ALTER TABLE post ADD COLUMN tags VARCHAR(200)"))
                        print('Added tags column to post table')
        except Exception as e:
            print(f'Schema migration note: {e}')
        
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