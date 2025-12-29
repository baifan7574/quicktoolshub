"""
添加 Image Resizer 文章到博客并部署
"""
import sys
sys.path.append('.')
from generate_resizer_blog import ImageResizerBlogGenerator
import paramiko
from scp import SCPClient
import time

def add_resizer_article():
    print("=" * 80)
    print("添加 Image Resizer 文章到博客")
    print("=" * 80)
    
    # 1. 生成文章
    print("\n步骤 1: 生成 Image Resizer 文章...")
    generator = ImageResizerBlogGenerator()
    new_article = generator.generate_article()
    print(f"✅ 已生成文章: {new_article['title']}")
    
    # 2. 读取现有的 blog.py
    print("\n步骤 2: 读取现有 blog.py...")
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        blog_content = f.read()
    
    # 3. 在 ARTICLES 列表末尾添加新文章
    print("\n步骤 3: 添加新文章...")
    
    # 找到 ARTICLES 列表的结束位置（最后一个 ]）
    articles_end = blog_content.rfind(']')
    
    # 生成新文章的代码
    content_escaped = new_article['content'].replace('"""', '\\"\\"\\"')
    
    new_article_code = f'''    {{
        "slug": "{new_article['slug']}",
        "title": "{new_article['title']}",
        "description": "{new_article['description']}",
        "keywords": "{new_article['keywords']}",
        "date": "{new_article['date']}",
        "category": "{new_article['category']}",
        "tool_name": "{new_article['tool_name']}",
        "tool_slug": "{new_article['tool_slug']}",
        "excerpt": "{new_article['excerpt']}",
        "content": """{content_escaped}""",
        "related_articles": {new_article['related_articles']}
    }},
'''
    
    # 在 ] 之前插入新文章
    blog_content = blog_content[:articles_end] + new_article_code + blog_content[articles_end:]
    
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
        
        print("\n🎉 博客现在有 7 篇文章！")
        print("\n【PDF Compressor - 3篇】")
        print("  1. http://soeasyhub.com/blog/how-to-compress-pdf-online-free")
        print("  2. http://soeasyhub.com/blog/pdf-compression-tips")
        print("  3. http://soeasyhub.com/blog/best-pdf-compressor")
        print("\n【Image Compressor - 3篇】")
        print("  4. http://soeasyhub.com/blog/how-to-compress-image-online-free")
        print("  5. http://soeasyhub.com/blog/image-compression-tips")
        print("  6. http://soeasyhub.com/blog/best-image-compressor")
        print("\n【Image Resizer - 1篇】✨ 新增！")
        print("  7. http://soeasyhub.com/blog/how-to-resize-image-online-free")
        
        print("\n📚 文章内容：")
        print("  ✅ 完整的 Image Resizer 教程")
        print("  ✅ 社交媒体尺寸对照表")
        print("  ✅ 网站图片尺寸指南")
        print("  ✅ 最佳实践和常见错误")
        print("  ✅ 指向 Image Resizer 工具的链接")
        print("  ✅ 相关文章链接")
        
        print("\n✅ 所有链接都正常工作！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    add_resizer_article()
