"""
Standardized tools.py with Base64 Encoder support
"""
from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase
import os

bp = Blueprint('tools', __name__, url_prefix='/tools')

def log_debug(msg):
    try:
        with open('/root/soeasyhub_v2/debug.txt', 'a') as f:
            f.write(msg + '\n')
    except:
        pass

def get_tools_list(category_slug=None, sort='popular', page=1, limit=100):
    supabase = get_supabase()
    tools_data = []
    try:
        if supabase:
            # We fetch more to ensure we have all tools for categorization accuracy
            query = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True)
            
            if sort == 'recent': query = query.order('created_at', desc=True)
            elif sort == 'alphabetical': query = query.order('name', desc=False)
            elif sort == 'most-used': query = query.order('use_count', desc=True)
            else: query = query.order('view_count', desc=True)
            
            result = query.execute()
            tools_data = result.data if result.data else []
            
            # CRITICAL: Filter out old duplicate tools that are being replaced by hardcoded versions
            unwanted_slugs = {'url-encoder'} 
            tools_data = [t for t in tools_data if t.get('slug') not in unwanted_slugs]
    except Exception as e:
        log_debug(f"Error fetching tools: {e}")
        pass
    
    # 强制添加硬编码工具
    hardcoded = [
        {
            "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
            "description": "Format, validate, and beautify JSON data instantly.", "view_count": 500, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9992, "name": "Base64 Encoder/Decoder", "slug": "base64-encoder",
            "description": "Encode and decode text to/from Base64 format securely.", "view_count": 300, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9993, "name": "URL Encoder/Decoder", "slug": "url-encoder-decoder",
            "description": "Encode and decode URLs with percent-encoding for safe transmission.", "view_count": 250, "category_id": 4, 
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        },
        {
            "id": 9994, "name": "Word Counter", "slug": "word-counter",
            "description": "Count words, characters, and paragraphs in real-time.", "view_count": 600, "category_id": 3, 
            "categories": {"name": "Text Tools", "slug": "text-tools"}
        }
    ]
    
    # 合并并去重
    existing_slugs = {t['slug'] for t in tools_data}
    for h in hardcoded:
        if h['slug'] not in existing_slugs:
            tools_data.append(h)

    # 过滤分类
    if category_slug and category_slug != 'all':
        tools_data = [t for t in tools_data if t.get('categories', {}).get('slug') == category_slug]

    return tools_data

def render_tools_page(tools_list, page=1, total_pages=1):
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    categories_data = []
    
    supabase = get_supabase()
    try:
        if supabase:
             categories = supabase.table('categories').select('*').order('name').execute()
             if categories.data: categories_data = categories.data
    except: pass
    
    if not categories_data:
        categories_data = [
            {"id": 1, "name": "Image Tools", "slug": "image-tools"},
            {"id": 2, "name": "PDF Tools", "slug": "pdf-tools"},
            {"id": 3, "name": "Text Tools", "slug": "text-tools"},
            {"id": 4, "name": "Developer Tools", "slug": "developer-tools"}
        ]

    # 动态重新计算所有工具的分类统计
    # 获取“所有”工具（不带过滤）
    all_active_tools = get_tools_list(category_slug='all')
    total_count = len(all_active_tools)
    
    # 计算每个分类的数量
    counts = {}
    for t in all_active_tools:
        c_slug = t.get('categories', {}).get('slug')
        if c_slug:
            counts[c_slug] = counts.get(c_slug, 0) + 1
    
    # 将统计结果写入 categories_data
    for cat in categories_data:
        cat['tool_count'] = counts.get(cat['slug'], 0)
    
    return render_template('tools/index.html', 
                          tools=tools_list, 
                          categories=categories_data, 
                          current_category=category_slug, 
                          current_sort=sort, 
                          page=page, 
                          total_pages=total_pages,
                          total_count=total_count)

@bp.route('')
def tools_list():
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    tools_list = get_tools_list(category_slug=category_slug, sort=sort)
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
        
    # Overrides for self-developed tools not in production DB yet
    if not tool:
        if slug == 'json-formatter':
            tool = {
                "id": 9991, "name": "JSON Formatter", "slug": "json-formatter",
                "description": "Format, validate, and beautify JSON data.",
                "short_description": "Format JSON",
                "view_count": 500, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'base64-encoder':
            tool = {
                "id": 9992, "name": "Base64 Encoder/Decoder", "slug": "base64-encoder",
                "description": "Encode and decode text to/from Base64 format securely.",
                "short_description": "Base64 Tool",
                "view_count": 300, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'url-encoder-decoder':
            tool = {
                "id": 9993, "name": "URL Encoder/Decoder", "slug": "url-encoder-decoder",
                "description": "Encode and decode URLs instantly.",
                "short_description": "URL Tool",
                "view_count": 250, "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
        elif slug == 'word-counter':
            tool = {
                "id": 9994, "name": "Word Counter", "slug": "word-counter",
                "description": "Accurate word and character counting tool.",
                "short_description": "Word Tool",
                "view_count": 600, "category_id": 3,
                "categories": {"name": "Text Tools", "slug": "text-tools"}
            }
    
    if not tool:
        return "Tool not found", 404
        
    related_tools = []
    return render_template('tools/detail.html', tool=tool, related_tools=related_tools)
