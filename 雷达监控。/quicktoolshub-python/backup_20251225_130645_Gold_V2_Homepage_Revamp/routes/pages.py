from flask import Blueprint, render_template

bp = Blueprint('pages', __name__)

@bp.route('/about')
def about():
    """关于我们页面"""
    return render_template('pages/about.html')

@bp.route('/contact')
def contact():
    """联系我们页面"""
    return render_template('pages/contact.html')

@bp.route('/privacy-policy')
def privacy_policy():
    """隐私政策页面"""
    return render_template('pages/privacy_policy.html')

@bp.route('/terms-of-service')
def terms_of_service():
    """服务条款页面"""
    return render_template('pages/terms_of_service.html')

@bp.route('/cookie-policy')
def cookie_policy():
    """Cookie政策页面"""
    return render_template('pages/cookie_policy.html')

@bp.route('/disclaimer')
def disclaimer():
    """免责声明页面"""
    return render_template('pages/disclaimer.html')

@bp.route('/search')
def search():
    """搜索页面"""
    from flask import request
    from utils.supabase_client import get_supabase
    
    query = request.args.get('q', '').strip()
    tools = []
    articles = []
    categories = []
    
    if query:
        supabase = get_supabase()
        
        # 搜索工具
        try:
            tools_result = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True).execute()
            if tools_result.data:
                # 简单过滤（因为 REST API 不支持 ilike）
                tools = [t for t in tools_result.data if query.lower() in (t.get('name', '') + ' ' + t.get('description', '') + ' ' + t.get('short_description', '')).lower()][:20]
        except:
            pass
        
        # 搜索文章
        try:
            articles_result = supabase.table('articles').select('*').eq('is_published', True).execute()
            if articles_result.data:
                articles = [a for a in articles_result.data if query.lower() in (a.get('title', '') + ' ' + a.get('content', '') + ' ' + a.get('excerpt', '')).lower()][:10]
        except:
            pass
        
        # 搜索分类
        try:
            categories_result = supabase.table('categories').select('*').execute()
            if categories_result.data:
                categories = [c for c in categories_result.data if query.lower() in (c.get('name', '') + ' ' + c.get('description', '')).lower()][:10]
        except:
            pass
    
    total_results = len(tools) + len(articles) + len(categories)
    
    return render_template('pages/search.html', 
                         query=query,
                         tools=tools,
                         articles=articles,
                         categories=categories,
                         total_results=total_results)

@bp.route('/categories')
def categories():
    """分类列表页面"""
    from utils.supabase_client import get_supabase
    
    supabase = get_supabase()
    categories_result = supabase.table('categories').select('*').order('tool_count', desc=True).execute()
    
    return render_template('pages/categories.html', 
                         categories=categories_result.data if categories_result.data else [])

@bp.route('/categories/<slug>')
def category_detail(slug):
    """分类详情页面"""
    from utils.supabase_client import get_supabase
    from routes.tools import get_tools_list
    
    supabase = get_supabase()
    category_result = supabase.table('categories').select('*').eq('slug', slug).single().execute()
    
    if not category_result.data:
        return "分类不存在", 404
    
    category = category_result.data
    tools = get_tools_list(category_slug=slug)
    
    return render_template('pages/category_detail.html', 
                         category=category,
                         tools=tools)

