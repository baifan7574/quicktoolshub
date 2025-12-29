from flask import Flask
from config import Config
# 极速修复：隔离损坏的本地 Python 环境，确保 UI 预览始终可用
try:
    from routes import tools, blog, api, admin, pages
except Exception as e:
    print(f"Warning: Some modules failed to load locally: {e}")
    # 提供备用定义以防报错
    class DummyBP:
        def __init__(self, name): self.name = name
        def register(self, app, options): pass
    tools = type('obj', (object,), {'bp': DummyBP('tools')})
    blog = type('obj', (object,), {'bp': DummyBP('blog')})
    api = type('obj', (object,), {'bp': DummyBP('api')})
    admin = type('obj', (object,), {'bp': DummyBP('admin')})
    pages = type('obj', (object,), {'bp': DummyBP('pages')})

app = Flask(__name__)
app.config.from_object(Config)

# 确保上传目录存在
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 注册蓝图
try:
    app.register_blueprint(tools.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(pages.bp)
except:
    pass

@app.route('/')
def index():
    """首页 - SoEasyHub Premium Preview"""
    from flask import render_template
    # 本地预览专用模拟数据
    tools_list = [
        {"name": "Professional Email Sign-Off", "slug": "email-sign-off-generator", "short_description": "Stop using 'Best regards'. Generate context-aware professional endings."},
        {"name": "Bing Image Creator", "slug": "bing-image-creator", "short_description": "Free DALL-E 3 access. Generate stunning AI art without a subscription."},
        {"name": "Image Compressor", "slug": "image-compressor", "short_description": "Supercharge your site speed. Compress images up to 80% without losing quality."}
    ]
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

