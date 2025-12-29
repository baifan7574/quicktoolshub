"""
Hello World Debug
"""
from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase

bp = Blueprint('tools', __name__, url_prefix='/tools')

# ... get_tools_list 省略 ... 
def get_tools_list(category_slug=None, sort='popular', page=1, limit=20):
    return [] # 暂时为空，不重要

@bp.route('')
def tools_list():
    return "Tools List"

@bp.route('/<slug>')
def tool_detail(slug):
    # 第一行直接返回，验证路由是否生效
    if slug == 'json-formatter':
        return "HELLO WORLD - JSON FORMATTER IS ALIVE!", 200
        
    return f"Slug received: {slug}", 404
