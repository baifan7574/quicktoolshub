import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Supabase 配置
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or ''
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or ''
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
    # 背景移除服务配置
    BACKGROUND_REMOVER_URL = os.environ.get('BACKGROUND_REMOVER_URL') or 'http://localhost:5000'
    
    # 其他配置
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

