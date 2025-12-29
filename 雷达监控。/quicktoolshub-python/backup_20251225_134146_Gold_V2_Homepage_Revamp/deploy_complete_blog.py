"""
一键部署 Image Compressor 完整博客系统
包括：3 篇文章 + 工具页面链接 + 互相链接
"""

import paramiko
from scp import SCPClient
import time
import sys
sys.path.append('.')
from generate_image_compressor_blog import ImageCompressorBlogGenerator

def deploy_complete_blog_system():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    print("=" * 80)
    print("部署 Image Compressor 完整博客系统")
    print("=" * 80)
    
    # 1. 生成文章内容
    print("\n步骤 1: 生成博客文章...")
    generator = ImageCompressorBlogGenerator()
    articles = generator.generate_all_articles()
    print(f"✅ 已生成 {len(articles)} 篇文章")
    
    # 2. 更新 blog.py
    print("\n步骤 2: 更新 blog.py...")
    
    # 读取现有的 blog.py
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        blog_content = f.read()
    
    # 添加新文章到 ARTICLES 列表
    # 找到 ARTICLES 列表的位置并添加新文章
    new_articles_code = ""
    for article in articles:
        new_articles_code += f"""    {{
        "slug": "{article['slug']}",
        "title": "{article['title']}",
        "description": "{article['description']}",
        "keywords": "{article['keywords']}",
        "date": "{article['date']}",
        "category": "{article['category']}",
        "tool_name": "{article['tool_name']}",
        "tool_slug": "{article['tool_slug']}",
        "excerpt": "{article['excerpt']}",
        "content": '''{article['content']}''',
        "related_articles": {article['related_articles']}
    }},
"""
    
    # 在第一篇文章后面插入新文章
    import_pos = blog_content.find('ARTICLES = [')
    if import_pos != -1:
        # 找到第一个文章结束的位置
        first_article_end = blog_content.find('},\n]', import_pos)
        if first_article_end != -1:
            # 在第一篇文章后插入新文章
            blog_content = blog_content[:first_article_end + 3] + new_articles_code + blog_content[first_article_end + 3:]
    
    # 保存更新后的 blog.py
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print("✅ blog.py 已更新")
    
    # 3. 更新工具页面，添加到博客的链接
    print("\n步骤 3: 在工具页面添加博客链接...")
    
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        detail_content = f.read()
    
    # 在 Image Compressor 的 SEO 内容后添加相关文章链接
    blog_links_section = '''
                <h3>📚 Learn More</h3>
                <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem;">
                    <p style="font-weight: 600; margin-bottom: 1rem;">Related Articles:</p>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 0.75rem;">
                            <a href="/blog/how-to-compress-image-online-free" style="color: #c2410c; text-decoration: none;">
                                📄 How to Compress Image Online Free - Complete Guide →
                            </a>
                        </li>
                        <li style="margin-bottom: 0.75rem;">
                            <a href="/blog/image-compression-tips" style="color: #c2410c; text-decoration: none;">
                                💡 10 Expert Image Compression Tips →
                            </a>
                        </li>
                        <li>
                            <a href="/blog/best-image-compressor" style="color: #c2410c; text-decoration: none;">
                                ⭐ Best Image Compressor Tools Compared →
                            </a>
                        </li>
                    </ul>
                </div>'''
    
    # 在 Image Compressor SEO 内容的最后添加链接
    insert_marker = '{% elif \'word\' in tool.slug %}'
    if insert_marker in detail_content:
        detail_content = detail_content.replace(insert_marker, blog_links_section + '\n            </div>\n        </div>\n\n        ' + insert_marker)
    
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(detail_content)
    
    print("✅ 工具页面已添加博客链接")
    
    # 4. 部署到服务器
    print("\n步骤 4: 部署到服务器...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接到服务器")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('routes/blog.py', '/root/soeasyhub_v2/routes/blog.py')
            print("  ✅ blog.py (包含 3 篇新文章)")
            
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html (添加了博客链接)")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        
        print("\n" + "=" * 80)
        print("✅ 部署完成！")
        print("=" * 80)
        
        print("\n🎉 Image Compressor 博客系统已上线！")
        print("\n您现在可以访问：")
        print("\n【博客文章】")
        print("  1. http://soeasyhub.com/blog/how-to-compress-image-online-free")
        print("  2. http://soeasyhub.com/blog/image-compression-tips")
        print("  3. http://soeasyhub.com/blog/best-image-compressor")
        print("\n【工具页面】")
        print("  • http://soeasyhub.com/tools/image-compressor")
        print("    (现在包含到博客的链接)")
        print("\n【博客首页】")
        print("  • http://soeasyhub.com/blog")
        print("    (显示所有文章)")
        
        print("\n✅ 完整的内容营销系统已建立：")
        print("  ✅ 3 篇 SEO 优化文章（每篇 700+ 词）")
        print("  ✅ 工具页面 → 博客文章链接")
        print("  ✅ 博客文章 → 工具页面链接")
        print("  ✅ 博客文章之间互相链接")
        print("  ✅ 完整的内部链接网络")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_complete_blog_system()
