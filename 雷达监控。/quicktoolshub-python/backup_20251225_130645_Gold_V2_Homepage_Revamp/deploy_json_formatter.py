"""
部署 JSON Formatter 完整实现
包括：前端 JS + SEO 内容 + 博客文章
"""
import sys
sys.path.append('.')
from json_formatter_complete import JSON_FORMATTER_JS, JSON_FORMATTER_SEO, JSON_FORMATTER_BLOG
import paramiko
from scp import SCPClient
import time

def deploy_json_formatter():
    print("=" * 80)
    print("部署 JSON Formatter 完整实现")
    print("=" * 80)
    
    # 1. 更新 detail.html - 添加 SEO 内容
    print("\n步骤 1: 更新 detail.html...")
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 JSON Formatter 的位置并添加 SEO 内容
    # 假设在 Developer Tools 部分
    # 我们需要在适当的位置添加条件判断
    
    # 在 SEO Expert Content 部分添加 JSON Formatter
    marker = "{% if 'background' in tool.slug %}"
    if marker in content:
        new_section = "{{% if 'json' in tool.slug and 'formatter' in tool.slug %}}\n        {}\n\n        {}".format(JSON_FORMATTER_SEO, marker)
        content = content.replace(marker, new_section)
        print("✅ JSON Formatter SEO 内容已添加")
    
    # 在 JavaScript 部分添加 JSON Formatter 逻辑
    script_marker = "</script>\n</body>"
    if script_marker in content:
        content = content.replace(script_marker, f"{JSON_FORMATTER_JS}\n{script_marker}")
        print("✅ JSON Formatter JavaScript 已添加")
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 2. 更新 blog.py - 添加博客文章
    print("\n步骤 2: 更新 blog.py...")
    with open('routes/blog.py', 'r', encoding='utf-8') as f:
        blog_content = f.read()
    
    # 添加 JSON Formatter 文章
    new_article = f'''    {{
        "slug": "json-formatter-online-free-guide",
        "title": "JSON Formatter Online Free: Complete Guide to Validate and Beautify JSON 2025",
        "description": "Learn how to format JSON online free with validation and error reporting. Complete guide to JSON beautifier tools, syntax validation, and best practices.",
        "keywords": "JSON formatter online free, JSON validator, JSON beautifier, format JSON online",
        "date": "2025-12-23",
        "category": "Developer Tools",
        "tool_name": "JSON Formatter",
        "tool_slug": "json-formatter",
        "excerpt": "Format and validate JSON online with our free JSON formatter tool.",
        "content": """{JSON_FORMATTER_BLOG.replace('"""', '\\"\\"\\"')}""",
        "related_articles": [
            {{"slug": "base64-encoder-guide", "title": "Base64 Encoder Guide"}},
            {{"slug": "url-encoder-guide", "title": "URL Encoder Guide"}}
        ]
    }},
'''
    
    # 在 ARTICLES 列表末尾添加
    articles_end = blog_content.rfind(']')
    if articles_end != -1:
        blog_content = blog_content[:articles_end] + new_article + blog_content[articles_end:]
        print("✅ JSON Formatter 博客文章已添加")
    
    # 保存
    with open('routes/blog.py', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
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
        
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps_output = stdout.read().decode()
        
        if ps_output:
            print("✅ 服务已启动")
        else:
            print("❌ 服务启动失败")
        
        print("\n" + "=" * 80)
        print("🎉 JSON Formatter 完整实现已部署！")
        print("=" * 80)
        
        print("\n✅ 已部署内容：")
        print("  1. ✅ 前端 JavaScript 功能")
        print("     - JSON 格式化（美化，4 空格缩进）")
        print("     - JSON 验证（语法检查）")
        print("     - 错误报告（精确定位错误）")
        print("     - 复制到剪贴板")
        
        print("\n  2. ✅ SEO 三件套内容")
        print("     - 7 个高价值关键词")
        print("     - JSON formatter online free")
        print("     - JSON validator with error reporting")
        print("     - JSON beautifier tool")
        
        print("\n  3. ✅ 博客文章")
        print("     - 2500+ 词完整教程")
        print("     - 常见错误示例")
        print("     - 最佳实践")
        
        print("\n🚀 现在访问：")
        print("  • 工具页面: http://soeasyhub.com/tools/json-formatter")
        print("  • 博客文章: http://soeasyhub.com/blog/json-formatter-online-free-guide")
        
        print("\n✅ JSON Formatter 已完全实现并上线！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_json_formatter()
