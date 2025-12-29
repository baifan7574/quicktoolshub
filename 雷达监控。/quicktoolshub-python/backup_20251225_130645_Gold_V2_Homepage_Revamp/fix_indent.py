"""
Fix IndentationError in blog.py
"""
import paramiko
from scp import SCPClient
import time

def fix_indent():
    print("修复 blog.py 缩进错误...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    # 下载
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_indent.py')
        
    # 读取
    with open('blog_indent.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"Total lines: {len(lines)}")
    
    # 我们知道错误在 1328 行 (大约)
    # 我们需要找到 `def blog_article(slug):` 这一行，然后修复下面的缩进
    # 标准缩进是 4 个空格
    
    new_lines = []
    in_function = False
    
    for i, line in enumerate(lines):
        if "def blog_article(slug):" in line:
            in_function = True
            new_lines.append(line) # def 行缩进不用动 (应该是 0)
            continue
            
        if in_function:
            # 这是一个函数体内的行
            # 如果是空行，保持原样
            if not line.strip():
                new_lines.append(line)
                continue
                
            # 必须以 4 个空格开头
            content = line.strip()
            new_lines.append(f"    {content}\n")
        else:
            new_lines.append(line)
            
    # 只对最后几行做这个处理太危险，可能会误伤。
    # 让我们只针对这几行具体的代码进行修复
    # 找到 1328 行附近的上下文
    
    # 重新读取，针对性修复
    target_idx = -1
    for i, line in enumerate(lines):
        if "article = next((a for a in ARTICLES" in line:
            target_idx = i
            break
            
    if target_idx != -1:
        print(f"Found target at line {target_idx+1}: {lines[target_idx]}")
        # 强制修正这一行及后续几行的缩进
        lines[target_idx] = "    article = next((a for a in ARTICLES if a['slug'] == slug), None)\n"
        
        # 下一行
        if target_idx + 1 < len(lines):
            lines[target_idx+1] = "    if not article:\n"
            
        # 再下一行
        if target_idx + 2 < len(lines):
            lines[target_idx+2] = '        return "Article not found", 404\n'
            
        # ... 后面的相关代码 ...
        # 为了保险，我们直接用之前的那段正确代码替换这几行
        
        # 找到函数结束位置（假设后面没代码了）
        func_body = """    article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not article:
        return "Article not found", 404
        
    related = []
    # Simple related logic
    try:
        if article.get('category'):
            related = [a for a in ARTICLES if a.get('category') == article['category'] and a['slug'] != slug][:3]
    except:
        pass
        
    return render_template('blog/article.html', article=article, related_articles=related)
"""
        # 我们把从 target_idx 开始的所有内容都替换掉
        # 因为 blog_article 应该是文件的最后一个函数
        final_lines = lines[:target_idx]
        final_lines.append(func_body)
        
        with open('blog_indent_fixed.py', 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
            
        print("缩已修复")
        
        # 上传
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('blog_indent_fixed.py', '/root/soeasyhub_v2/routes/blog.py')
            
        print("重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(2)
        cmd = "cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
        ssh.exec_command(cmd)
        time.sleep(5)
        
        # 检查日志
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        if stdout.read().decode():
            print("✅ 服务启动成功！")
        else:
            print("❌ 服务依然失败，查看日志...")
            stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/soeasyhub_v2/gunicorn.log")
            print(stdout.read().decode())

    else:
        print("❌没找到出错的行！")
        
    ssh.close()

if __name__ == "__main__":
    fix_indent()
