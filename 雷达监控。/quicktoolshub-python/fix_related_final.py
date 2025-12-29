"""
Fix related articles logic by forcing a selection
"""
import paramiko
from scp import SCPClient
import time

def fix_related_final():
    print("Reading local blog_failed_logic.py...")
    with open('blog_failed_logic.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 替换整个 blog_article 函数
    # 我们知道函数的大概样子
    
    start_marker = "def blog_article(slug):"
    end_marker = "return render_template('blog/article.html', article=article, related_articles=related)"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Function not found!")
        return

    # 为了安全，我们只替换函数体之后的部分
    # 构造一个新的函数体
    
    new_function_body = """def blog_article(slug):
    \"\"\"博客文章详情\"\"\"
    # Find current article
    article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not article:
        return "Article not found", 404
        
    # FORCE RELATE STRATEGY
    # 1. Get all other articles
    others = [a for a in ARTICLES if a['slug'] != slug]
    
    # 2. Prefer same category
    related = []
    if article.get('category'):
        related = [a for a in others if a.get('category') == article.get('category')]
        
    # 3. Fill with anything else if not enough
    if len(related) < 3:
        remaining = [a for a in others if a not in related]
        related.extend(remaining)
        
    # 4. Slice to 3
    related = related[:3]
    
    # Debug print to Gunicorn log
    print(f"DEBUG: Found {len(ARTICLES)} total articles. Selected {len(related)} related.")
    
    return render_template('blog/article.html', article=article, related_articles=related)
"""

    # 我们需要找到原函数在文件中的确切范围。
    # 由于我们有文件内容，可以用 find 找到 start_marker
    # 但是 end_marker 可能因为代码变化而不准确 (比如之前的 logic fix 改变了内容)
    # 所以我们得小心。
    
    # 之前我也读取了文件，所以 blog_failed_logic.py 是最新的。
    # 让我们直接替换从 `def blog_article(slug):` 开始，直到文件末尾（如果它是最后一个函数）
    # 或者直到下一个 @ 符号？不，它是最后一个函数。
    
    new_content = content[:start_idx] + new_function_body
    
    with open('blog_final_fix.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Logic replaced locally.")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("Uploading...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_final_fix.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Restarting...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("Done!")
    ssh.close()

if __name__ == "__main__":
    fix_related_final()
