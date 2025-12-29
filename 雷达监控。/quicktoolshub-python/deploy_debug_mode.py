"""
Add debug output to blog.py
"""
import paramiko
from scp import SCPClient
import time

def add_debug_mode():
    print("Reading local blog_assignment_fix.py...")
    with open('blog_assignment_fix.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Reuse the same replacement strategy
    start_marker = "def blog_article(slug):"
    start_idx = content.find(start_marker)

    new_function_body = """def blog_article(slug):
    \"\"\"博客文章详情\"\"\"
    from flask import request, jsonify
    
    # 1. Find Current Article
    raw_article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not raw_article:
        return "Article not found", 404
        
    article = raw_article.copy()
        
    # 2. Strategy: Force Fill
    others = [a for a in ARTICLES if a['slug'] != slug]
    
    # Priority 1: Same category
    related = []
    if article.get('category'):
        related = [a for a in others if a.get('category') == article.get('category')]
        
    # Priority 2: Fill rest
    if len(related) < 3:
        remaining = [a for a in others if a not in related]
        related.extend(remaining)
        
    # Slice
    related = related[:3]
    
    # 3. Assign to article dict for template
    article['related_articles'] = related
    
    # --- DEBUG MODE ---
    if request.args.get('debug'):
        return jsonify({
            'current_article': article['title'],
            'total_articles': len(ARTICLES),
            'others_count': len(others),
            'related_count': len(related),
            'related_items': related
        })
    # ------------------
    
    return render_template('blog/article.html', article=article, related_articles=related)
"""

    new_content = content[:start_idx] + new_function_body
    
    with open('blog_debug_mode.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Uploading debug version...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_debug_mode.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Nuking pycache and restarting...")
    ssh.exec_command("find /root/soeasyhub_v2 -name '__pycache__' -type d -exec rm -rf {} +")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("Debug mode active.")
    ssh.close()

if __name__ == "__main__":
    add_debug_mode()
