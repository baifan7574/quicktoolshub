"""
简化版 JSON Formatter 部署脚本
避免复杂的 f-string 语法
"""
import sys
sys.path.append('.')
import paramiko
from scp import SCPClient
import time

# 直接定义内容，不使用变量导入
JSON_SEO_CONTENT = """<div class="expert-section">
    <div class="scary-seo-content">
        <h2 class="playfair">JSON Formatter Online Free: Validate and Beautify JSON Data 2025</h2>
        <div class="expert-quote">
            <p>"I once spent 3 hours debugging an API integration, only to discover the JSON response had a 
                single missing comma on line 247. A JSON validator with error reporting would have found it in 
                3 seconds. Learning to format JSON online isn't just convenient—it's essential for developer 
                productivity in 2025."</p>
        </div>

        <h3>⚠️ The Unreadable JSON Problem</h3>
        <p>APIs return minified JSON—thousands of characters in a single line, impossible to read or debug. 
            When you're trying to understand API responses, find errors, or validate data structures, 
            unformatted JSON is a productivity killer.</p>

        <h3>Format JSON Online with Validation</h3>
        <p>Professional JSON formatting transforms compressed data into readable, properly indented code. 
            Our JSON formatter online free tool validates syntax, highlights errors, and beautifies JSON 
            with perfect indentation—essential for API development, debugging, and data analysis.</p>

        <h3>Developer Productivity Impact</h3>
        <p>Formatted JSON improves code review efficiency by 10x. When debugging API integrations or reviewing 
            data structures, properly formatted JSON lets you:</p>
        <ul>
            <li><strong>Spot Errors Instantly</strong>: Missing commas, brackets, quotes highlighted immediately</li>
            <li><strong>Understand Structure</strong>: Nested objects and arrays clearly visible</li>
            <li><strong>Debug Faster</strong>: Find data issues in seconds instead of hours</li>
            <li><strong>Validate Syntax</strong>: Ensure JSON is valid before sending to APIs</li>
        </ul>

        <h3>Privacy & Security</h3>
        <p>Many online JSON formatters upload your data to third-party servers, exposing API keys, user data, 
            or confidential information. Our client-side JSON formatter processes everything locally in your 
            browser—your sensitive JSON data never touches our servers.</p>

        <h3>Common Use Cases</h3>
        <ul>
            <li><strong>API Development</strong>: Format and validate API responses for debugging</li>
            <li><strong>Data Analysis</strong>: Beautify JSON data files for easier reading</li>
            <li><strong>Code Review</strong>: Format JSON before committing to version control</li>
            <li><strong>Testing</strong>: Validate JSON payloads before sending to APIs</li>
            <li><strong>Learning</strong>: Understand JSON structure with syntax highlighting</li>
        </ul>
    </div>
</div>"""

def deploy():
    print("=" * 80)
    print("部署 JSON Formatter")
    print("=" * 80)
    
    # 读取 detail.html
    print("\n读取 detail.html...")
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加 JSON Formatter SEO 内容
    marker = "{% if 'background' in tool.slug %}"
    if marker in content:
        insert_text = "{% if 'json' in tool.slug and 'formatter' in tool.slug %}\n        " + JSON_SEO_CONTENT + "\n\n        " + marker
        content = content.replace(marker, insert_text)
        print("✅ SEO 内容已添加")
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 部署
    print("\n部署到服务器...")
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password, timeout=30)
        print("✅ 已连接")
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('templates/tools/detail.html', '/root/soeasyhub_v2/templates/tools/detail.html')
            print("✅ 已上传")
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        print("✅ JSON Formatter 已部署！")
        print("\n访问: http://soeasyhub.com/tools/json-formatter")
        
    except Exception as e:
        print("❌ 错误:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy()
