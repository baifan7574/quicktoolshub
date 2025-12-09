from supabase import create_client, Client
from config import Config

# 创建 Supabase 客户端
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def get_supabase():
    """获取 Supabase 客户端"""
    return supabase

