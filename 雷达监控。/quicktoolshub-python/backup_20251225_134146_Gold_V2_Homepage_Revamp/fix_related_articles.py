"""
Fix empty related articles by adding fallback logic
"""
import paramiko
from scp import SCPClient
import time

def fix_related_articles():
    print("Downloading blog.py...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    local_path = 'blog_related_fix.py'
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', local_path)
        
    print("Modifying logic...")
    with open(local_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Find the logic inside blog_article function
    # Look for: related = [a for a in ARTICLES if a.get('category')
    
    new_lines = []
    
    # We will replace the simple related logic with a smarter one
    # We identify the block by looking for "related = []" inside the function
    
    inside_function = False
    replaced = False
    
    for i, line in enumerate(lines):
        if "def blog_article(slug):" in line:
            inside_function = True
        
        # Determine strict matching logic to replace
        if inside_function and "related = []" in line and not replaced:
            # We found the start of the logic block. 
            # We will skip the next few lines that constituted the old logic
            # and insert new logic.
            
            # Insert new robust logic
            indent = "    "
            new_lines.append(f"{indent}related = []\n")
            new_lines.append(f"{indent}# Try to find articles in same category first\n")
            new_lines.append(f"{indent}if article.get('category'):\n")
            new_lines.append(f"{indent}    related = [a for a in ARTICLES if a.get('category') == article['category'] and a['slug'] != slug]\n")
            new_lines.append(f"\n")
            new_lines.append(f"{indent}# Fallback: If no related articles (or too few), fill with recent articles\n")
            new_lines.append(f"{indent}if len(related) < 3:\n")
            new_lines.append(f"{indent}    # Get other articles excluding current one and already selected ones\n")
            new_lines.append(f"{indent}    existing_slugs = [r['slug'] for r in related]\n")
            new_lines.append(f"{indent}    others = [a for a in ARTICLES if a['slug'] != slug and a['slug'] not in existing_slugs]\n")
            new_lines.append(f"{indent}    related.extend(others[:3 - len(related)])\n")
            new_lines.append(f"\n")
            new_lines.append(f"{indent}# Limit to 3\n")
            new_lines.append(f"{indent}related = related[:3]\n")
            
            replaced = True
            
        elif inside_function and replaced:
            # Skip lines until we hit the return statement or end of try/except block mentioned in previous fix
            # The previous code was:
            # related = []
            # # Simple related logic
            # try:
            #     if article.get('category'):
            #         related = [a for a in ARTICLES if a.get('category') == article['category'] and a['slug'] != slug][:3]
            # except:
            #     pass
            
            # We want to keep the 'return' statement.
            if "return render_template" in line:
                new_lines.append(line)
                inside_function = False # Exit function scope tracking roughly
            elif "try:" in line or "except:" in line or "pass" in line or "related =" in line or "if article.get" in line:
                # These are the lines we are removing/replacing
                continue
            else:
                # Keep other lines (like empty lines)
                if line.strip() == "": continue
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open('blog_related_fixed.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print("Logic updated. Uploading...")
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('blog_related_fixed.py', '/root/soeasyhub_v2/routes/blog.py')
        
    print("Restarting...")
    ssh.exec_command("pkill -9 gunicorn || true")
    time.sleep(2)
    cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ssh.exec_command(cmd)
    
    time.sleep(5)
    print("Done! Related articles should now be populated.")
    ssh.close()

if __name__ == "__main__":
    fix_related_articles()
