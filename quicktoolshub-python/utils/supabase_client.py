import requests
from config import Config

# 使用 REST API 而不是 Python SDK（避免密钥格式问题）
class SupabaseClient:
    def __init__(self, url, key):
        self.url = url.rstrip('/')
        self.key = key
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
    
    def table(self, table_name):
        return SupabaseTable(self.url, table_name, self.headers)

class SupabaseTable:
    def __init__(self, base_url, table_name, headers):
        self.base_url = base_url
        self.table_name = table_name
        self.headers = headers
        self.url = f"{base_url}/rest/v1/{table_name}"
    
    def select(self, columns='*'):
        self.columns = columns
        return self
    
    def eq(self, column, value):
        if not hasattr(self, 'params'):
            self.params = {}
        self.params[f'{column}'] = f'eq.{value}'
        return self
    
    def neq(self, column, value):
        if not hasattr(self, 'params'):
            self.params = {}
        self.params[f'{column}'] = f'neq.{value}'
        return self
    
    def order(self, column, desc=False):
        if not hasattr(self, 'params'):
            self.params = {}
        order_dir = 'desc' if desc else 'asc'
        self.params['order'] = f'{column}.{order_dir}'
        return self
    
    def range(self, start, end):
        if not hasattr(self, 'params'):
            self.params = {}
        self.params['range'] = f'{start}-{end}'
        return self
    
    def limit(self, count):
        if not hasattr(self, 'params'):
            self.params = {}
        self.params['limit'] = str(count)
        return self
    
    def single(self):
        self.single_result = True
        return self
    
    def execute(self):
        response = requests.get(self.url, headers=self.headers, params=getattr(self, 'params', {}))
        response.raise_for_status()
        
        class Result:
            def __init__(self, data):
                self.data = data
        
        if hasattr(self, 'single_result') and self.single_result:
            data = response.json()
            return Result(data if isinstance(data, dict) else (data[0] if data else None))
        else:
            return Result(response.json())

# 延迟初始化 Supabase 客户端
_supabase_client = None

def get_supabase():
    """获取 Supabase 客户端（使用 REST API）"""
    global _supabase_client
    if _supabase_client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        _supabase_client = SupabaseClient(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _supabase_client

