"""
Fix related articles by assigning to article dictionary key
"""
import paramiko
from scp import SCPClient
import time

def fix_related_assignment():
    print("Reading local blog_failed_logic.py...")
    with open('blog_failed_logic.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Reuse the same replacement strategy but with the updated assignment
    
    start_marker = "def blog_article(slug):"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Function not found!")
        return

    new_function_body = """def blog_article(slug):
    \"\"\"博客文章详情\"\"\"
    # Find current article
    # Copy it to avoid modifying the global list permanently or race conditions
    raw_article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not raw_article:
        return "Article not found", 404
        
    article = raw_article.copy()
        
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
    
    # CRITICAL FIX: Assign back to article dictionary because template uses article.related_articles
    article['related_articles'] = related
    
    # Debug print
    print(f"DEBUG: Article {slug} has {len(related)} related items.")
    
    return render_template('blog/article.html', article=article, related_articles=related)
"""

    new_content = content[:start_idx] + new_function_body
    
    with open('blog_assignment_fix.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Logic updated with assignment. Uploading...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_assignment_fix.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Restarting...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("Done!")
    ssh.close()

if __name__ == "__main__":
    fix_related_assignment()
