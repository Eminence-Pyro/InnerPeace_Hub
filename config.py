import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / '.env')

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    
    # Database
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///innerpeacehub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pool — prevents dropped connection errors
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,        # tests connection before using it
        "pool_recycle": 300,          # recycles connections every 5 minutes
        "pool_size": 5,
        "max_overflow": 2,
        "connect_args": {
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 5,
            "keepalives_count": 3,
        }
    }
    
    # CKEditor
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_FILE_UPLOADER = 'admin.upload'
    CKEDITOR_ENABLE_CSRF = False
    CKEDITOR_TOOLBAR = [
        ['Undo', 'Redo'],
        ['Format', 'FontSize'],
        ['Bold', 'Italic', 'Underline', 'StrikeThrough'],
        ['TextColor', 'BGColor'],
        ['Link', 'Unlink', 'Anchor'],
        ['Image', 'Table'],
        ['NumberedList', 'BulletedList', 'Indent', 'Outdent'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ['Source'],
        ['RemoveFormat', 'ShowBlocks']
    ]
    CKEDITOR_EXTRA_ALLOWED_CONTENT = 'div(*); span(*); a[*]{*}(*); img[*]{*}(*)'
    
    # File upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB upload limit
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 2592000  # 30 days in seconds


class DevelopmentConfig(Config):
    """Local machine settings"""
    SESSION_COOKIE_SECURE = False  # Works on plain HTTP locally


class ProductionConfig(Config):
    """Live server settings"""
    SESSION_COOKIE_SECURE = True  # Requires HTTPS on Render