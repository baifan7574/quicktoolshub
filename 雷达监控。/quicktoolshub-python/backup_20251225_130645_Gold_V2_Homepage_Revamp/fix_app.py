"""
Remove try-except block in app.py to expose real errors
"""
import paramiko
from scp import SCPClient
import time

def fix_app_py():
    print("Patching app.py to remove try-except...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    # 我们直接写一个新的 app.py，内容基于刚才读取的，但去掉 try-except
    new_app_content = """from flask import Flask
from config import Config

# 直接导入，不捕获异常，让错误暴露出来！
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
    \"\"\"首页 - SoEasyHub Premium Preview\"\"\"
    from flask import render_template
    # 本地预览专用模拟数据
    tools_list = [
        {"name": "Background Remover", "slug": "background-remover", "short_description": "Elite AI background removal with expert privacy protection."},
        {"name": "PDF Compressor", "slug": "pdf-compressor", "short_description": "Professional grade PDF optimization for legal and corporate use."},
        {"name": "PDF to Word", "slug": "pdf-to-word", "short_description": "Preserve every pixel and font with our AI conversion engine."}
    ]
    return render_template('index.html', tools=tools_list)

@app.route('/health')
def health():
    \"\"\"健康检查\"\"\"
    return {'status': 'healthy'}, 200

@app.route('/sitemap.xml')
def sitemap():
    \"\"\"生成 sitemap.xml\"\"\"
    from flask import Response
    from utils.supabase_client import get_supabase

    supabase = get_supabase()

    # 获取所有工具
    try:
        tools = supabase.table('tools').select('slug').eq('is_active', True).execute()
        tool_slugs = [t['slug'] for t in (tools.data or [])]
    except:
        tool_slugs = []

    # 获取所有已发布文章
    try:
        articles = supabase.table('articles').select('slug').eq('is_published', True).execute()
        article_slugs = [a['slug'] for a in (articles.data or [])]
    except:
        article_slugs = []

    # 生成 XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'

    # 首页
    xml += '  <url><loc>https://soeasyhub.com/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\\n'
    xml += '  <url><loc>https://soeasyhub.com/tools</loc><changefreq>daily</changefreq><priority>0.9</priority></url>\\n'
    xml += '  <url><loc>https://soeasyhub.com/blog</loc><changefreq>daily</changefreq><priority>0.9</priority></url>\\n'

    # 工具页面
    for slug in tool_slugs:
        xml += f'  <url><loc>https://soeasyhub.com/tools/{slug}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\\n'

    # 文章页面
    for slug in article_slugs:
        xml += f'  <url><loc>https://soeasyhub.com/blog/{slug}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>\\n'

    xml += '</urlset>'

    return Response(xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    \"\"\"生成 robots.txt\"\"\"
    from flask import Response
    robots_txt = \"\"\"User-agent: *
Allow: /
Sitemap: https://soeasyhub.com/sitemap.xml
\"\"\"
    return Response(robots_txt, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
"""
    
    with open('app_fixed.py', 'w', encoding='utf-8') as f:
        f.write(new_app_content)
        
    # 上传
    print("Uploading app.py...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('app_fixed.py', '/root/soeasyhub_v2/app.py')
        
    print("Restarting server...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    time.sleep(5)
    
    # 检查状态
    print("Checking status...")
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    ps = stdout.read().decode()
    if ps:
        print("✅ Server started! This means imports are clean.")
    else:
        print("❌ Server failed to start! Checking logs for IMPORT ERROR...")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
        print(stdout.read().decode())
        
    ssh.close()

if __name__ == "__main__":
    fix_app_py()
