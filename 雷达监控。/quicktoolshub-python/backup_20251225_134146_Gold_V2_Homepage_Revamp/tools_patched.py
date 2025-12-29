from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase

bp = Blueprint('tools', __name__, url_prefix='/tools')

def get_tools_list(category_slug=None, sort='popular', page=1, limit=20):
    """获取工具列表"""
    supabase = get_supabase()
    
    tools_data = []
    try:
        if not supabase:
             raise Exception("No supabase client")
             
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
        tools_data = result.data if result.data else []
        
    except Exception as e:
        print(f"Database Error (Showing Mock Data): {e}")
        # 如果数据库连接失败，返回模拟数据以供演示
        tools_data = [
            {
                "name": "Background Remover",
                "slug": "background-remover",
                "description": "Remove image backgrounds automatically with one click. Free, private, and secure by SoEasyHub.",
                "short_description": "Remove image backgrounds instantly.",
                "view_count": 1205,
                "tool_type": "local",
                "category_id": 1,
                "categories": {"name": "Image Tools", "slug": "image-tools"}
            },
            {
                "name": "PDF Compressor",
                "slug": "pdf-compressor", 
                "description": "Reduce PDF file size while maintaining high quality standards.",
                "short_description": "Compress PDF files efficiently.",
                "view_count": 890,
                "tool_type": "local",
                "categories": {"name": "PDF Tools", "slug": "pdf-tools"}
            }
        ]
    

    # 强制添加 JSON Formatter (如果列表中还没有)
    has_json = False
    for t in tools_data:
        if t.get('slug') == 'json-formatter':
            has_json = True
            break
            
    if not has_json and (not category_slug or category_slug == 'all' or category_slug == 'developer-tools'):
        json_tool = {
            "id": 999,
            "name": "JSON Formatter",
            "slug": "json-formatter",
            "description": "Format, validate, and beautify JSON data. Perfect for developers and API testing.",
            "short_description": "Format and validate JSON instantly.",
            "view_count": 0,
            "tool_type": "local",
            "category_id": 4,  # 假设 4 是 Developer Tools
            "categories": {"name": "Developer Tools", "slug": "developer-tools"}
        }
        tools_data.append(json_tool)

    return tools_data

def render_tools_page(tools_list, page=1, total_pages=1):
    """渲染工具列表页面"""
    category_slug = request.args.get('category', 'all')
    sort = request.args.get('sort', 'popular')
    
    # 获取所有分类和工具
    supabase = get_supabase()
    categories_data = []
    
    try:
        if supabase:
            # 获取所有分类
            categories = supabase.table('categories').select('*').order('name').execute()
            
            # 获取所有工具（用于统计）
            all_tools = supabase.table('tools').select('category_id').eq('is_active', True).execute()
            
            # 统计每个分类的工具数量
            category_counts = {}
            if all_tools.data:
                for tool in all_tools.data:
                    cat_id = tool.get('category_id')
                    if cat_id:
                        category_counts[cat_id] = category_counts.get(cat_id, 0) + 1
            
            # 为每个分类添加工具数量
            if categories.data:
                for category in categories.data:
                    category['tool_count'] = category_counts.get(category['id'], 0)
                    categories_data.append(category)
        else:
            # 备用分类数据
            categories_data = [
                {"name": "Image Tools", "slug": "image-tools", "tool_count": 4},
                {"name": "PDF Tools", "slug": "pdf-tools", "tool_count": 3},
                {"name": "Text Tools", "slug": "text-tools", "tool_count": 2},
                {"name": "Developer Tools", "slug": "developer-tools", "tool_count": 3}
            ]
    except Exception as e:
        print(f"Error fetching categories: {e}")
        # 使用备用数据
        categories_data = [
            {"name": "Image Tools", "slug": "image-tools", "tool_count": 4},
            {"name": "PDF Tools", "slug": "pdf-tools", "tool_count": 3},
            {"name": "Text Tools", "slug": "text-tools", "tool_count": 2},
            {"name": "Developer Tools", "slug": "developer-tools", "tool_count": 3}
        ]
    
    return render_template('tools/index.html',
                         tools=tools_list,
                         categories=categories_data,
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
    
    # PDF Merger 使用专用模板
    if slug == 'pdf-merger':
        return render_template('tools/pdf_merger.html')
    
    # PDF Splitter 使用专用模板
    if slug == 'pdf-splitter':
        return render_template('tools/pdf_splitter.html')
    
    supabase = get_supabase()
    
    # 获取工具信息
    tool_result = supabase.table('tools').select('*, categories(name, slug)').eq('slug', slug).eq('is_active', True).single().execute()
    
    if not tool_result.data:
        # 手动处理 JSON Formatter
        if slug == 'json-formatter':
            tool = {
                "id": 999,
                "name": "JSON Formatter",
                "slug": "json-formatter",
                "description": "Format, validate, and beautify JSON data.",
                "view_count": 0,
                "category_id": 4,
                "categories": {"name": "Developer Tools", "slug": "developer-tools"}
            }
            # 获取相关工具 (模拟)
            related_tools = []
            return render_template('tools/detail.html', tool=tool, related_tools=related_tools)
            
        return "Tool not found", 404
    
    tool = tool_result.data
    
    # 更新浏览次数
    try:
        current_views = tool.get('view_count', 0) or 0
        supabase.table('tools').update({'view_count': current_views + 1}).eq('id', tool['id']).execute()
    except:
        pass  # 如果更新失败，不影响页面显示
    
    # 获取同分类的其他工具（相关工具）
    related_tools = []
    if tool.get('category_id'):
        try:
            related_result = supabase.table('tools').select('*, categories(name, slug)').eq('category_id', tool['category_id']).eq('is_active', True).neq('id', tool['id']).limit(6).execute()
            related_tools = related_result.data if related_result.data else []
        except:
            pass
    
    return render_template('tools/detail.html', tool=tool, related_tools=related_tools)

