"""
Debug tools.py with file logging
"""
from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase
import os

bp = Blueprint('tools', __name__, url_prefix='/tools')

# 模块加载立即写入
try:
    with open('/root/soeasyhub_v2/module_loaded.txt', 'w') as f:
        f.write('Tools module loaded successfully\n')
except:
    pass

def log_debug(msg):
    try:
        with open('/root/soeasyhub_v2/debug.txt', 'a') as f:
            f.write(msg + '\n')
    except:
        pass

def get_tools_list(category_slug=None, sort='popular', page=1, limit=20):
    supabase = get_supabase()
    tools_data = []
    try:
        if supabase:
            query = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True)
            if category_slug and category_slug != 'all':
                category = supabase.table('categories').select('id').eq('slug', category_slug).single().execute()
                if category.data: query = query.eq('category_id', category.data['id'])
            if sort == 'recent': query = query.order('created_at', desc=True)
            elif sort == 'alphabetical': query = query.order('name', desc=False)
            elif sort == 'most-used': query = query.order('use_count', desc=True)
            else: query = query.order('view_count', desc=True)
            offset = (page - 1) * limit
            result = query.range(offset, offset + limit - 1).execute()
            tools_data = result.data if result.data else []
    except: pass
    
    # 强制添加
    has_json = False
    for t in tools_data:
        if t.get('slug') == 'json-formatter': has_json = True; break
    if not has_json:
        tools_data.append({
            "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
            "description": "Format JSON", "view_count": 0, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        })
    return tools_data

def render_tools_page(tools_list, page=1, total_pages=1):
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    categories_data = []
    try:
        supabase = get_supabase()
        if supabase:
             categories = supabase.table('categories').select('*').order('name').execute()
             if categories.data: categories_data = categories.data
    except: pass
    
    return render_template('tools/index.html', tools=tools_list, categories=categories_data, current_category=category_slug, current_sort=sort, page=page, total_pages=total_pages)

@bp.route('')
def tools_list():
    tools_list = get_tools_list()
    return render_tools_page(tools_list)

@bp.route('/<slug>')
def tool_detail(slug):
    log_debug(f"DEBUG: tool_detail called with slug='{slug}'")
    
    if slug == 'pdf-merger': return render_template('tools/pdf_merger.html')
    if slug == 'pdf-splitter': return render_template('tools/pdf_splitter.html')
    
    supabase = get_supabase()
    tool = None
    try:
        tool_result = supabase.table('tools').select('*, categories(name, slug)').eq('slug', slug).eq('is_active', True).single().execute()
        if tool_result.data: tool = tool_result.data
    except Exception as e:
        log_debug(f"DB Error: {e}")
        pass
        
    if not tool:
        log_debug(f"Tool not found in DB. Checking override for '{slug}'")
        if slug == 'json-formatter':
            log_debug("MATCHED json-formatter override!")
            tool = {
                "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
                "description": "Format, validate, and beautify JSON data.",
                "short_description": "Format JSON",
                "view_count": 500, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
    
    if not tool:
        log_debug("Returning 404")
        return "Tool not found", 404
        
    related_tools = []
    
    log_debug("Rendering template...")
    return render_template('tools/detail.html', tool=tool, related_tools=related_tools)
