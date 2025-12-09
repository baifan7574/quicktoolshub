from flask import Flask
from config import Config
from routes import tools, blog, api, admin, pages

app = Flask(__name__)
app.config.from_object(Config)

# 确保上传目录存在
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 注册蓝图
app.register_blueprint(tools.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(api.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(pages.bp)

@app.route('/')
def index():
    """首页"""
    from flask import render_template
    from routes.tools import get_tools_list
    tools_list = get_tools_list(limit=12)
    return render_template('index.html', tools=tools_list)

@app.route('/health')
def health():
    """健康检查"""
    return {'status': 'healthy'}, 200

@app.route('/sitemap.xml')
def sitemap():
    """生成 sitemap.xml"""
    from flask import Response
    from utils.supabase_client import get_supabase
    
    supabase = get_supabase()
    
    # 获取所有工具
    tools = supabase.table('tools').select('slug').eq('is_active', True).execute()
    tool_slugs = [t['slug'] for t in (tools.data or [])]
    
    # 获取所有已发布文章
    articles = supabase.table('articles').select('slug').eq('is_published', True).execute()
    article_slugs = [a['slug'] for a in (articles.data or [])]
    
    # 生成 XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # 首页
    xml += '  <url><loc>https://soeasyhub.com/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
    xml += '  <url><loc>https://soeasyhub.com/tools</loc><changefreq>daily</changefreq><priority>0.9</priority></url>\n'
    xml += '  <url><loc>https://soeasyhub.com/blog</loc><changefreq>daily</changefreq><priority>0.9</priority></url>\n'
    
    # 工具页面
    for slug in tool_slugs:
        xml += f'  <url><loc>https://soeasyhub.com/tools/{slug}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    
    # 文章页面
    for slug in article_slugs:
        xml += f'  <url><loc>https://soeasyhub.com/blog/{slug}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\n'
    
    xml += '</urlset>'
    
    return Response(xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """生成 robots.txt"""
    from flask import Response
    robots_txt = """User-agent: *
Allow: /
Sitemap: https://soeasyhub.com/sitemap.xml
"""
    return Response(robots_txt, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)

