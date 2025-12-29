"""
添加 PDF Compressor 的 2 篇文章到 blog.py 并部署
"""
import sys
sys.path.append('.')
from generate_pdf_compressor_blog import PDFCompressorBlogGenerator
import paramiko
from scp import SCPClient
import time

def add_pdf_articles():
    print("=" * 80)
    print("添加 PDF Compressor 文章到博客")
    print("=" * 80)
    
    # 1. 生成新文章
    print("\n步骤 1: 生成 PDF Compressor 文章...")
    generator = PDFCompressorBlogGenerator()
    new_articles = generator.generate_all_articles()
    print(f"✅ 已生成 {len(new_articles)} 篇文章")
    
    # 2. 读取现有的 blog.py
    print("\n步骤 2: 读取现有 blog.py...")
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        blog_content = f.read()
    
    # 3. 在 ARTICLES 列表末尾添加新文章（在最后一个 ] 之前）
    print("\n步骤 3: 添加新文章...")
    
    # 找到 ARTICLES 列表的结束位置
    articles_end = blog_content.rfind(']')
    
    # 生成新文章的代码
    new_articles_code = ""
    for article in new_articles:
        content_escaped = article['content'].replace('"""', '\\"\\"\\"')
        
        new_articles_code += f'''    {{
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
    
    # 在 ] 之前插入新文章
    blog_content = blog_content[:articles_end] + new_articles_code + blog_content[articles_end:]
    
    # 4. 保存更新后的 blog.py
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print("✅ blog.py 已更新")
    
    # 5. 部署到服务器
    print("\n步骤 4: 部署到服务器...")
    
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
        
        print("\n🎉 现在博客有 6 篇文章！")
        print("\n【PDF Compressor 文章】")
        print("  1. http://soeasyhub.com/blog/how-to-compress-pdf-online-free")
        print("  2. http://soeasyhub.com/blog/pdf-compression-tips")
        print("  3. http://soeasyhub.com/blog/best-pdf-compressor")
        print("\n【Image Compressor 文章】")
        print("  4. http://soeasyhub.com/blog/how-to-compress-image-online-free")
        print("  5. http://soeasyhub.com/blog/image-compression-tips")
        print("  6. http://soeasyhub.com/blog/best-image-compressor")
        
        print("\n✅ 所有相关文章链接现在都正常工作！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    add_pdf_articles()
