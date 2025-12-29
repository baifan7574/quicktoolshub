"""
手术修复 blog.py
"""
import sys
sys.path.append('.')
from json_formatter_complete import JSON_FORMATTER_BLOG
import paramiko
from scp import SCPClient
import time

def surgical_fix():
    print("开始手术修复 blog.py...")
    
    # 1. 读取坏掉的文件
    with open('blog_broken.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 2. 定位切断点
    # 错误的代码大概在文件末尾，看起来像这样：
    # ... JSON文章内容 ...
    #     "related_articles": []
    # },
    # ] == slug), None)
    
    # 我们需要把 "JSON文章内容" 之前的部分（ARTICLES列表主体）保留
    # 把 "JSON文章内容" 提取出来
    # 把 "] == slug), None)" 之后的部分（如果有）保留，并重建前面的路由逻辑
    
    # 找到 JSON Formatter 文章的开始
    article_key = '"slug": "json-formatter-online-free-guide"'
    start_pos = content.find(article_key)
    # 往回找它的开始大括号
    start_bracket = content.rfind('{', 0, start_pos)
    
    if start_pos == -1:
        print("❌ 没找到插入的文章！无法自动修复。")
        return

    # 前半部分：直到插入文章之前（应该是上一篇文章的结束逗号后面）
    # 但要注意，之前的脚本可能把 ARTICLES 列表的闭合 ] 给弄没了或者弄乱了
    
    # 我们直接把整个文件截断到 start_bracket 之前
    # 然后追加我们正确的 JSON 文章
    # 然后追加正确的 ARTICLES 列表结束符
    # 然后追加正确的路由函数
    
    part1 = content[:start_bracket].rstrip()
    # 确保 part1 结尾有逗号
    if not part1.strip().endswith(','):
        part1 += ','
        
    # JSON 文章内容（我们直接用之前定义好的，保证纯净）
    article_content = JSON_FORMATTER_BLOG.replace('"""', '\\"\\"\\"')
    
    json_article = f'''
    {{
        "slug": "json-formatter-online-free-guide",
        "title": "JSON Formatter Online Free: Complete Guide to Validate and Beautify JSON 2025",
        "description": "Learn how to format JSON online free with validation and error reporting.",
        "keywords": "JSON formatter online free, JSON validator, JSON beautifier",
        "date": "2025-12-23",
        "category": "Developer Tools",
        "tool_name": "JSON Formatter",
        "tool_slug": "json-formatter",
        "excerpt": "Format and validate JSON online with our free JSON formatter tool.",
        "content": """{article_content}""",
        "related_articles": []
    }}
'''

    # 路由函数部分
    # 原来的代码可能是：
    # article = next((a for a in ARTICLES if a['slug'] == slug), None)
    # 注意：前面的 @blog.route 可能还在 part1 里吗？
    # 让我们检查 part1 的末尾，看看是否切断了 ARTICLES 列表
    
    # 假设 ARTICLES 列表之前的结构是正常的
    
    router_code = """
]

@blog_bp.route('/<slug>')
def article_detail(slug):
    article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not article:
        return "Article not found", 404
    return render_template('blog/article.html', article=article)
"""
    
    # 组合新文件
    new_content = part1 + json_article + router_code
    
    # 写入文件
    with open('blog_fixed.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ 文件已从头重建")
    
    # 3. 上传并重启
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_fixed.py', '/root/soeasyhub_v2/routes/blog.py')
        print("✅ blog.py 已上传")
        
    print("🔄 重启服务...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
    time.sleep(5)
    
    # 验证
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
    if stdout.read().decode():
        print("✅ 服务启动成功！")
        print("访问: http://soeasyhub.com/tools/json-formatter")
    else:
        print("❌ 服务启动失败，请检查日志")

    ssh.close()

if __name__ == "__main__":
    surgical_fix()
