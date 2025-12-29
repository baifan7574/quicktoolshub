"""
一键修复：生成完整的 blog.py 并部署
"""
import sys
sys.path.append('.')
from generate_image_compressor_blog import ImageCompressorBlogGenerator
import paramiko
from scp import SCPClient
import time

def create_complete_blog_py():
    """生成完整的 blog.py 文件"""
    
    # 生成 Image Compressor 文章
    generator = ImageCompressorBlogGenerator()
    image_articles = generator.generate_all_articles()
    
    # 创建完整的 blog.py 内容
    blog_py_content = '''from flask import Blueprint, render_template
from datetime import datetime

bp = Blueprint('blog', __name__, url_prefix='/blog')

# 文章数据
ARTICLES = [
'''
    
    # 添加 PDF Compressor 文章
    blog_py_content += '''    {
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

<p>PDF compression is the process of reducing the file size of a PDF document while maintaining acceptable quality. This is achieved by optimizing images, removing unnecessary data, and using efficient encoding methods.</p>

<h3>Why Compress PDF Files?</h3>

<ul>
    <li><strong>Email Attachments</strong>: Most email services limit attachment sizes to 25MB</li>
    <li><strong>Faster Uploads</strong>: Smaller files upload and download faster</li>
    <li><strong>Storage Savings</strong>: Reduce cloud storage costs</li>
    <li><strong>Better Performance</strong>: Compressed PDFs load faster in browsers</li>
</ul>

<h2>How to Compress PDF Online Free with SoEasyHub</h2>

<h3>Step 1: Upload Your PDF</h3>
<p>Visit our <a href="/tools/pdf-compressor">PDF Compressor tool</a> and click the upload area. You can drag and drop your file or click to browse.</p>

<h3>Step 2: Choose Compression Level</h3>
<p>Select your desired compression level based on your needs.</p>

<h3>Step 3: Download Compressed PDF</h3>
<p>Click "Compress PDF" and wait a few seconds. Your compressed file will be ready to download immediately.</p>

<h2>Why Choose SoEasyHub for PDF Compression?</h2>

<h3>🔒 Complete Privacy</h3>
<p>Unlike many online tools, SoEasyHub processes your files locally in your browser. Your documents never touch our servers, ensuring complete privacy and security.</p>

<h3>⚡ Lightning Fast</h3>
<p>Our optimized compression algorithms work quickly, even with large files. Most compressions complete in under 10 seconds.</p>

<h3>💰 Completely Free</h3>
<p>No hidden costs, no subscription fees, no watermarks. Just free, professional-quality PDF compression.</p>

<h2>Conclusion</h2>

<p>Learning how to <strong>compress PDF online free</strong> is easier than you think. With SoEasyHub, you can reduce file sizes quickly, securely, and without any cost.</p>

<p>Ready to compress your PDF files? Try our tool now and experience the difference!</p>
""",
        "related_articles": [
            {"slug": "pdf-compression-tips", "title": "10 Expert PDF Compression Tips"},
            {"slug": "best-pdf-compressor", "title": "Best PDF Compressor Tools Compared"}
        ]
    },
'''
    
    # 添加 3 篇 Image Compressor 文章
    for article in image_articles:
        # 转义内容中的引号
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
    
    return blog_py_content

def deploy_fixed_blog():
    """部署修复后的 blog.py"""
    
    print("=" * 80)
    print("修复并部署博客文章")
    print("=" * 80)
    
    # 1. 生成完整的 blog.py
    print("\n步骤 1: 生成完整的 blog.py...")
    blog_content = create_complete_blog_py()
    
    # 保存到本地
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print("✅ blog.py 已生成（包含 4 篇文章）")
    
    # 2. 部署到服务器
    print("\n步骤 2: 部署到服务器...")
    
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
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n" + "=" * 80)
        print("✅ 部署完成！")
        print("=" * 80)
        
        print("\n🎉 所有文章已上线！")
        print("\n【可访问的文章】")
        print("  1. http://soeasyhub.com/blog/how-to-compress-pdf-online-free")
        print("  2. http://soeasyhub.com/blog/how-to-compress-image-online-free")
        print("  3. http://soeasyhub.com/blog/image-compression-tips")
        print("  4. http://soeasyhub.com/blog/best-image-compressor")
        print("\n【博客首页】")
        print("  • http://soeasyhub.com/blog")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_fixed_blog()
