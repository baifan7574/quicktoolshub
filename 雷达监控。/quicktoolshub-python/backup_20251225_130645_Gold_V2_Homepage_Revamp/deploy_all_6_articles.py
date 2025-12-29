"""
生成包含所有 6 篇文章的完整 blog.py
"""
import sys
sys.path.append('.')
from generate_image_compressor_blog import ImageCompressorBlogGenerator
from generate_pdf_compressor_blog import PDFCompressorBlogGenerator
import paramiko
from scp import SCPClient
import time

def create_complete_blog_with_all_articles():
    print("=" * 80)
    print("生成包含所有 6 篇文章的完整 blog.py")
    print("=" * 80)
    
    # 1. 生成所有文章
    print("\n步骤 1: 生成所有文章...")
    
    # PDF Compressor 文章
    pdf_gen = PDFCompressorBlogGenerator()
    pdf_article_1 = {
        "slug": "how-to-compress-pdf-online-free",
        "title": "How to Compress PDF Online Free - Complete Guide 2025",
        "description": "Learn how to compress PDF files online for free. Step-by-step guide with expert tips.",
        "keywords": "compress PDF, reduce PDF size, PDF compressor",
        "date": "2025-12-22",
        "category": "PDF Tools",
        "tool_name": "PDF Compressor",
        "tool_slug": "pdf-compressor",
        "excerpt": "Learn the best way to compress PDF files online for free. Our complete guide covers everything from basic compression to advanced techniques.",
        "content": """
<h1 class="playfair">How to Compress PDF Online Free - Complete Guide 2025</h1>

<p>Are you struggling with large PDF files? Whether you need to email a document, upload it to a website, or simply save storage space, learning how to <strong>compress PDF files online free</strong> is an essential skill.</p>

<h2>What is PDF Compression?</h2>

<p>PDF compression is the process of reducing the file size of a PDF document while maintaining acceptable quality.</p>

<h2>Why Choose SoEasyHub for PDF Compression?</h2>

<h3>🔒 Complete Privacy</h3>
<p>Unlike many online tools, SoEasyHub processes your files locally in your browser. Your documents never touch our servers, ensuring complete privacy and security.</p>

<p>Ready to compress your PDF files? <a href="/tools/pdf-compressor">Try our tool now</a>!</p>
""",
        "related_articles": [
            {"slug": "pdf-compression-tips", "title": "10 Expert PDF Compression Tips"},
            {"slug": "best-pdf-compressor", "title": "Best PDF Compressor Tools Compared"}
        ]
    }
    
    pdf_articles = [pdf_article_1] + pdf_gen.generate_all_articles()
    
    # Image Compressor 文章
    img_gen = ImageCompressorBlogGenerator()
    img_articles = img_gen.generate_all_articles()
    
    all_articles = pdf_articles + img_articles
    
    print(f"✅ 已生成 {len(all_articles)} 篇文章")
    print(f"  - PDF Compressor: {len(pdf_articles)} 篇")
    print(f"  - Image Compressor: {len(img_articles)} 篇")
    
    # 2. 生成 blog.py 内容
    print("\n步骤 2: 生成 blog.py 文件...")
    
    blog_py_content = '''from flask import Blueprint, render_template
from datetime import datetime

bp = Blueprint('blog', __name__, url_prefix='/blog')

# 文章数据
ARTICLES = [
'''
    
    # 添加所有文章
    for article in all_articles:
        content_escaped = article['content'].replace('"""', '\\"\\"\\"')
        
        blog_py_content += f'''    {{
        "slug": "{article['slug']}",
        "title": "{article['title']}",
        "description": "{article['description']}",
        "keywords": "{article['keywords']}",
        "date": "{article['date']}",
        "category": "{article['category']}",
        "tool_name": "{article['tool_name']}",
        "tool_slug": "{article['tool_slug']}",
        "excerpt": "{article['excerpt']}",
        "content": """{content_escaped}""",
        "related_articles": {article['related_articles']}
    }},
'''
    
    # 完成 blog.py
    blog_py_content += ''']

@bp.route('')
def blog_index():
    """博客首页"""
    return render_template('blog/index.html', articles=ARTICLES)

@bp.route('/<slug>')
def blog_article(slug):
    """博客文章详情"""
    article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not article:
        return "Article not found", 404
    return render_template('blog/article.html', article=article)
'''
    
    # 保存到本地
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_py_content)
    
    print("✅ blog.py 已生成")
    
    # 3. 部署到服务器
    print("\n步骤 3: 部署到服务器...")
    
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('routes/blog.py', '/root/soeasyhub_v2/routes/blog.py')
            print("  ✅ blog.py 已上传")
        
        # 验证语法
        print("\n验证 Python 语法...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && python3 -c 'import routes.blog; print(f\"Found {len(routes.blog.ARTICLES)} articles\")'")
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error:
            print(f"❌ 语法错误: {error}")
            return
        else:
            print(f"✅ 语法正确: {output.strip()}")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        # 验证服务启动
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps_output = stdout.read().decode()
        
        if ps_output:
            print("✅ 服务已启动")
        else:
            print("❌ 服务启动失败")
        
        print("\n" + "=" * 80)
        print("✅ 部署完成！")
        print("=" * 80)
        
        print("\n🎉 博客现在有 6 篇完整文章！")
        print("\n【PDF Compressor - 3篇】")
        print("  1. http://soeasyhub.com/blog/how-to-compress-pdf-online-free")
        print("  2. http://soeasyhub.com/blog/pdf-compression-tips")
        print("  3. http://soeasyhub.com/blog/best-pdf-compressor")
        print("\n【Image Compressor - 3篇】")
        print("  4. http://soeasyhub.com/blog/how-to-compress-image-online-free")
        print("  5. http://soeasyhub.com/blog/image-compression-tips")
        print("  6. http://soeasyhub.com/blog/best-image-compressor")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    create_complete_blog_with_all_articles()
