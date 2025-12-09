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
        self.headers = headers.copy()  # 复制 headers，避免修改原始
        self.url = f"{base_url}/rest/v1/{table_name}"
        self.params = {}
        self.single_result = False
        self.select_columns = '*'
        self.range_header = None
    
    def select(self, columns='*'):
        self.select_columns = columns
        return self
    
    def eq(self, column, value):
        # PostgREST 格式：column=eq.value
        self.params[column] = f'eq.{value}'
        return self
    
    def neq(self, column, value):
        self.params[column] = f'neq.{value}'
        return self
    
    def order(self, column, desc=False):
        order_dir = 'desc' if desc else 'asc'
        if 'order' in self.params:
            self.params['order'] += f',{column}.{order_dir}'
        else:
            self.params['order'] = f'{column}.{order_dir}'
        return self
    
    def range(self, start, end):
        # Range 应该作为 HTTP 头发送，格式：Range: items=start-end
        self.range_header = f'items={start}-{end}'
        return self
    
    def limit(self, count):
        # 如果使用 range，就不需要 limit
        if not self.range_header:
            self.params['limit'] = str(count)
        return self
    
    def single(self):
        self.single_result = True
        return self
    
    def execute(self):
        # 构建查询参数
        query_params = {}
        
        # select 参数
        if self.select_columns != '*':
            query_params['select'] = self.select_columns
        
        # 其他查询参数（过滤、排序等）
        for key, value in self.params.items():
            query_params[key] = value
        
        # 构建请求头
        request_headers = self.headers.copy()
        
        # Range 作为 HTTP 头
        if self.range_header:
            request_headers['Range'] = self.range_header
        
        # 发送请求
        response = requests.get(self.url, headers=request_headers, params=query_params)
        response.raise_for_status()
        
        class Result:
            def __init__(self, data):
                self.data = data
        
        data = response.json()
        
        # 处理 single 结果
        if self.single_result:
            if isinstance(data, list):
                return Result(data[0] if data else None)
            else:
                return Result(data if data else None)
        else:
            # 确保返回列表
            if isinstance(data, list):
                return Result(data)
            else:
                return Result([data] if data else [])

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

