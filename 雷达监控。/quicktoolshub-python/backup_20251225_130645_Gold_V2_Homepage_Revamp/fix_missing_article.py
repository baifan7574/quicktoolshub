"""
Inject JSON Article into blog.py safely
"""
import paramiko
from scp import SCPClient
import time

def inject_article():
    print("Downloading blog.py...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_missing_article.py')
        
    print("Injecting article locally...")
    with open('blog_missing_article.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Article Data
    new_article = """    {
        "slug": "json-formatter-online-free-guide",
        "title": "JSON Formatter Online Free: Complete Guide to Validate and Beautify JSON 2025",
        "description": "Learn how to format JSON online free with validation and error reporting. The ultimate guide for developers to beautify and minify JSON data securely.",
        "keywords": "JSON formatter online free, JSON validator, JSON beautifier, minify JSON, API debugging",
        "date": "2025-12-23",
        "category": "Developer Tools",
        "tool_name": "JSON Formatter",
        "tool_slug": "json-formatter",
        "excerpt": "Format and validate JSON online with our free JSON formatter tool. Learn best practices for API debugging and data structure validation.",
        "content": \"\"\"
<h1 class="playfair">JSON Formatter Online Free: Complete Guide to Validate and Beautify JSON 2025</h1>
<p class="lead">Processing raw JSON data shouldn't be a headache. Discover how standardizing your JSON workflow can save hours of debugging time and prevent critical API errors.</p>

<h2>Why JSON Formatting Matters</h2>
<p>JSON (JavaScript Object Notation) is the language of the web. But when APIs return minified responses—collapsed into a single line without spaces—it becomes readable only to machines. For developers, this is a nightmare.</p>
<p>A missing comma or an unclosed bracket in a 10,000-character line is like finding a needle in a haystack. This is where a <strong>JSON Formatter Online Free</strong> tool becomes indispensable.</p>

<h2>Key Features of Our JSON Tool</h2>
<ul>
    <li><strong>Instant Validation</strong>: Detect syntax errors immediately with line number reporting.</li>
    <li><strong>Smart Indentation</strong>: Choose between 2 spaces, 4 spaces, or tabs to match your coding style.</li>
    <li><strong>Privacy First</strong>: All processing happens in your browser. Your sensitive API keys and data never leave your device.</li>
    <li><strong>Minification</strong>: Reverse the process by compressing JSON for production deployment to save bandwidth.</li>
</ul>

<h2>Common JSON Errors We Solve</h2>
<p>Even senior developers make syntax mistakes. Our validator catches:</p>
<ul>
    <li>Trailing commas (invalid in standard JSON)</li>
    <li>Single quotes (must be double quotes)</li>
    <li>Missing keys quotes</li>
    <li>Unmatched braces <code>{}</code> or brackets <code>[]</code></li>
</ul>

<h2>Best Practices for API Debugging</h2>
<p>When integrating 3rd party APIs like Stripe or Google Maps, always run their response through a formatter. Seeing the nested structure clearly allows you to identifying the data path (e.g., <code>response.data.items[0].id</code>) much faster than guessing.</p>

<p>Start using our <a href="/tools/json-formatter">JSON Formatter</a> today and reclaim your productivity.</p>
\"\"\"
    },
"""

    # 找到插入点
    # 我们寻找 ARTICLES = [ ... ] 的结尾
    # 既然 ARTICLES 是一个列表，它以 `]` 结束。
    # 我们可以找 `bp = Blueprint` 前面的那个 `]`。
    
    # 让我们找最后一个出现的 `]` ??? 不，太冒险。
    # 让我们找 `bp = Blueprint`，然后往回找最近的一个 `]`。
    
    bp_index = content.find("bp = Blueprint")
    if bp_index == -1:
        print("Error: Could not find Blueprint definition")
        return

    # 在 bp_index 之前找最后一个 `]`
    # 为了保险，我们搜索 ARTICLES 列表的定义
    # 或者直接插在倒数第二个 `]` 之前？(如果是 list of dicts)
    
    # 最稳妥的方法：找到 `ARTICLES = [`，然后通过 counting braces 来找到结尾？
    # 或者，我们直接插在 `ARTICLES = [` 之后！成为第一个元素！
    # 这样最简单，只要找到 `ARTICLES = [` 即可
    
    target_str = "ARTICLES = ["
    insert_pos = content.find(target_str)
    
    if insert_pos == -1:
        print("Error: Could not find ARTICLES list")
        return
        
    insert_point = insert_pos + len(target_str)
    
    # 插入
    new_content = content[:insert_point] + "\n" + new_article + content[insert_point:]
    
    with open('blog_repaired.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Article inserted successfully.")
    
    # 上传
    print("Uploading...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_repaired.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Restarting...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("Done!")
    ssh.close()

if __name__ == "__main__":
    inject_article()
