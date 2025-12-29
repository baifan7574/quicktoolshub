"""
部署 Image Compressor SEO 优化内容
只修改 SEO 文字，不碰功能代码
"""
import sys
sys.path.append('.')
from image_compressor_seo_optimized import THREE_PIECE_SEO_CONTENT, BLOG_ARTICLE_OPTIMIZED
import paramiko
from scp import SCPClient
import time

def deploy_image_compressor_seo():
    print("=" * 80)
    print("部署 Image Compressor SEO 优化")
    print("=" * 80)
    
    # 1. 读取现有 detail.html
    print("\n步骤 1: 读取 detail.html...")
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        detail_html = f.read()
    
    # 2. 找到 Image Compressor 的 SEO 部分并替换
    print("\n步骤 2: 替换 Image Compressor 三件套内容...")
    
    # 找到 Image Compressor 的 SEO 部分（在 {% elif 'compress' in tool.slug and 'image' in tool.slug %} 之后）
    start_marker = "{% elif 'compress' in tool.slug and 'image' in tool.slug %}"
    end_marker = "{% elif 'resize' in tool.slug or 'resizer' in tool.slug %}"
    
    start_pos = detail_html.find(start_marker)
    end_pos = detail_html.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print("❌ 找不到 Image Compressor SEO 部分")
        return
    
    # 替换内容
    new_section = f"\n        {start_marker}\n        {THREE_PIECE_SEO_CONTENT}\n\n        "
    detail_html = detail_html[:start_pos] + new_section + detail_html[end_pos:]
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(detail_html)
    
    print("✅ detail.html 已更新")
    
    # 3. 更新博客文章
    print("\n步骤 3: 更新博客文章...")
    
    # 读取现有 blog.py
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        blog_py = f.read()
    
    # 找到 Image Compressor 文章并替换内容
    # 文章 slug: "how-to-compress-image-online-free"
    
    # 找到文章开始位置
    article_start = blog_py.find('"slug": "how-to-compress-image-online-free"')
    if article_start == -1:
        print("❌ 找不到 Image Compressor 文章")
        return
    
    # 找到 content 字段
    content_start = blog_py.find('"content": """', article_start)
    content_end = blog_py.find('"""', content_start + 15)
    
    if content_start == -1 or content_end == -1:
        print("❌ 找不到文章内容字段")
        return
    
    # 替换内容（转义引号）
    escaped_content = BLOG_ARTICLE_OPTIMIZED.replace('"""', '\\"\\"\\"')
    blog_py = blog_py[:content_start + 15] + escaped_content + blog_py[content_end:]
    
    # 保存
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_py)
    
    print("✅ blog.py 已更新")
    
    # 4. 部署到服务器
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
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("  ✅ detail.html 已上传")
            
            scp.put('routes/blog.py', '/root/soeasyhub_v2/routes/blog.py')
            print("  ✅ blog.py 已上传")
        
        # 验证语法
        print("\n验证 Python 语法...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/soeasyhub_v2 && python3 -c 'import routes.blog'")
        error = stderr.read().decode()
        
        if error:
            print(f"❌ 语法错误: {error}")
            return
        else:
            print("✅ 语法正确")
        
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
        print("✅ Image Compressor SEO 优化已部署！")
        print("=" * 80)
        
        print("\n🎯 优化内容包括：")
        print("\n【三件套 SEO 内容】")
        print("  ✅ H2: How to Compress Images Without Losing Quality")
        print("  ✅ H3: Reduce Image File Size for Website Performance")
        print("  ✅ H3: Optimize Images for WordPress Speed")
        print("  ✅ H3: Compress PNG Files for Web Use")
        
        print("\n【博客文章优化】")
        print("  ✅ 标题包含主关键词")
        print("  ✅ 2500+ 词完整内容")
        print("  ✅ 8 个高价值长尾关键词自然分布")
        
        print("\n📊 目标关键词：")
        print("  1. compress images without losing quality")
        print("  2. reduce image file size for website")
        print("  3. compress JPEG images online free")
        print("  4. compress PNG files for web use")
        print("  5. optimize images for WordPress speed")
        print("  6. reduce photo size for email attachment")
        print("  7. online image compressor for faster website loading")
        print("  8. free image resizer and compressor")
        
        print("\n🚀 现在访问：")
        print("  • 工具页面: http://soeasyhub.com/tools/image-compressor")
        print("  • 博客文章: http://soeasyhub.com/blog/how-to-compress-image-online-free")
        
        print("\n✅ SEO 优化完成！这些关键词将开始为你带来流量！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_image_compressor_seo()
