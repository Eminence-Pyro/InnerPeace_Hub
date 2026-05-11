import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    
    # Database
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///innerpeacehub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CKEditor
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_FILE_UPLOADER = 'upload'
    CKEDITOR_ENABLE_CSRF = False
    
    # File upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB upload limit
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
