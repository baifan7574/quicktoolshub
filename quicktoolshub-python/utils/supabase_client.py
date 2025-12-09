from supabase import create_client, Client
from config import Config

# 延迟初始化 Supabase 客户端
_supabase_client = None

def get_supabase():
    """获取 Supabase 客户端（延迟初始化）"""
    global _supabase_client
    if _supabase_client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        _supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _supabase_client

