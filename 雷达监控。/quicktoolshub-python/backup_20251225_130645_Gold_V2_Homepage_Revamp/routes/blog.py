from flask import Blueprint, render_template, request
from utils.supabase_client import get_supabase
import markdown

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('')
def blog_list():
    """博客列表页面"""
    supabase = get_supabase()
    category = request.args.get('category', '')
    page = int(request.args.get('page', 1))
    limit = 20
    offset = (page - 1) * limit
    
    # 构建查询
    query = supabase.table('articles').select('*').eq('is_published', True).order('published_at', desc=True)
    
    if category:
        query = query.eq('category', category)
    
    result = query.range(offset, offset + limit - 1).execute()
    
    # 获取分类列表
    categories = supabase.table('articles').select('category').eq('is_published', True).execute()
    unique_categories = list(set([cat['category'] for cat in categories.data if cat.get('category')]))
    
    return render_template('blog/index.html',
                         articles=result.data if result.data else [],
                         categories=unique_categories,
                         current_category=category,
                         page=page)

@bp.route('/<slug>')
def blog_detail(slug):
    """博客文章详情页面"""
    supabase = get_supabase()
    
    article = supabase.table('articles').select('*').eq('slug', slug).eq('is_published', True).single().execute()
    
    if not article.data:
        return "文章不存在", 404
    
    # 将 Markdown 转换为 HTML
    article_data = article.data.copy()
    if article_data.get('content'):
        article_data['content'] = markdown.markdown(article_data['content'])
    
    return render_template('blog/detail.html', article=article_data)

