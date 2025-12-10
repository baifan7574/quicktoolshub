from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from utils.supabase_client import get_supabase
from datetime import datetime
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

# 简单的管理员验证（可以通过环境变量配置密码）
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'

def check_admin():
    """检查是否为管理员"""
    return session.get('admin_logged_in') == True

def require_admin():
    """要求管理员登录"""
    if not check_admin():
        return redirect('/admin/login')

@bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """管理员登录"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin/blog')
        else:
            return render_template('admin/login.html', error='密码错误')
    return render_template('admin/login.html')

@bp.route('/logout')
def admin_logout():
    """管理员登出"""
    session.pop('admin_logged_in', None)
    return redirect('/')

@bp.route('/blog')
def admin_blog_list():
    """后台博客列表"""
    if not check_admin():
        return redirect('/admin/login')
    
    supabase = get_supabase()
    articles = supabase.table('articles').select('*').order('created_at', desc=True).execute()
    
    return render_template('admin/blog_list.html', articles=articles.data if articles.data else [])

@bp.route('/blog/new')
def admin_blog_new():
    """创建新文章"""
    if not check_admin():
        return redirect('/admin/login')
    return render_template('admin/blog_new.html')

@bp.route('/blog/<id>/edit')
def admin_blog_edit(id):
    """编辑文章"""
    if not check_admin():
        return redirect('/admin/login')
    
    supabase = get_supabase()
    article = supabase.table('articles').select('*').eq('id', id).single().execute()
    
    if not article.data:
        return "文章不存在", 404
    
    return render_template('admin/blog_edit.html', article=article.data)

@bp.route('/api/articles', methods=['POST'])
def create_article():
    """创建文章 API"""
    supabase = get_supabase()
    data = request.json
    
    article_data = {
        'title': data.get('title'),
        'slug': data.get('slug'),
        'excerpt': data.get('excerpt'),
        'content': data.get('content'),
        'category': data.get('category'),
        'tags': data.get('tags', []),
        'featured_image': data.get('featured_image', ''),
        'is_published': data.get('is_published', False),
        'published_at': datetime.now().isoformat() if data.get('is_published') else None,
    }
    
    result = supabase.table('articles').insert(article_data).execute()
    
    return jsonify(result.data[0] if result.data else {}), 201

@bp.route('/api/articles/<id>', methods=['PATCH'])
def update_article(id):
    """更新文章 API"""
    supabase = get_supabase()
    data = request.json
    
    article_data = {
        'title': data.get('title'),
        'slug': data.get('slug'),
        'excerpt': data.get('excerpt'),
        'content': data.get('content'),
        'category': data.get('category'),
        'tags': data.get('tags', []),
        'featured_image': data.get('featured_image', ''),
        'is_published': data.get('is_published', False),
    }
    
    if data.get('is_published') and not data.get('published_at'):
        article_data['published_at'] = datetime.now().isoformat()
    elif data.get('published_at'):
        article_data['published_at'] = data.get('published_at')
    
    result = supabase.table('articles').update(article_data).eq('id', id).execute()
    
    return jsonify(result.data[0] if result.data else {}), 200

