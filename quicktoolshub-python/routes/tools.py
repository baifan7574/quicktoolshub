from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase

bp = Blueprint('tools', __name__, url_prefix='/tools')

def get_tools_list(category_slug=None, sort='popular', page=1, limit=20):
    """获取工具列表"""
    supabase = get_supabase()
    
    # 构建查询
    query = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True)
    
    # 分类筛选
    if category_slug and category_slug != 'all':
        # 先获取分类 ID
        category = supabase.table('categories').select('id').eq('slug', category_slug).single().execute()
        if category.data:
            query = query.eq('category_id', category.data['id'])
    
    # 排序
    if sort == 'recent':
        query = query.order('created_at', desc=True)
    elif sort == 'alphabetical':
        query = query.order('name', desc=False)
    elif sort == 'most-used':
        query = query.order('use_count', desc=True)
    else:  # popular
        query = query.order('view_count', desc=True)
    
    # 分页
    offset = (page - 1) * limit
    result = query.range(offset, offset + limit - 1).execute()
    
    return result.data if result.data else []

def render_tools_page(tools_list, page=1, total_pages=1):
    """渲染工具列表页面"""
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    
    # 获取所有分类
    supabase = get_supabase()
    categories = supabase.table('categories').select('*').order('name').execute()
    
    return render_template('tools/index.html',
                         tools=tools_list,
                         categories=categories.data if categories.data else [],
                         current_category=category_slug,
                         current_sort=sort,
                         page=page,
                         total_pages=total_pages)

@bp.route('')
def tools_list():
    """工具列表页面"""
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    page = int(request.args.get('page', 1))
    limit = 20
    
    tools_list = get_tools_list(category_slug, sort, page, limit)
    
    # 计算总页数（简化版，实际需要获取总数）
    total_pages = 1
    
    return render_tools_page(tools_list, page, total_pages)

@bp.route('/<slug>')
def tool_detail(slug):
    """工具详情页面"""
    supabase = get_supabase()
    
    # 获取工具信息
    tool = supabase.table('tools').select('*, categories(name, slug)').eq('slug', slug).eq('is_active', True).single().execute()
    
    if not tool.data:
        return "工具不存在", 404
    
    return render_template('tools/detail.html', tool=tool.data)

