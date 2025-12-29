"""
修复 blog.py 的语法错误
1. 下载
2. 修复（删除最后可能有问题的部分，重新正确添加）
3. 上传
4. 重启
"""
import paramiko
from scp import SCPClient
import time

def fix_blog():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("43.130.229.184", username="root", password="baifan100100", timeout=30)
    
    print("下载 blog.py...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('/root/soeasyhub_v2/routes/blog.py', 'blog_broken.py')
    
    # 读取并修复
    with open('blog_broken.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找错误点。通常是因为插入位置不对。
    # 我们知道 ARTICLES 是一个列表。
    # 关键是看文件末尾。
    print(f"文件长度: {len(content)}")
    print("文件末尾 200 字符:")
    print(content[-200:])
    
    # 如果是因为之前的脚本在 ']' 处插入，可能导致了结构混乱
    # 让我们尝试恢复到一个已知的良好状态
    # 找到 倒数第二个 "}," （上一个文章的结束）
    # 然后追加我们新的文章，并正确封闭列表
    
    # 策略：如果文件末尾乱了，我们尝试重构 ARTICLES 列表的结尾
    
    # 简单粗暴但有效的方法：
    # 找到 "ARTICLES = [" ... 找到所有的 "slug": "..." 
    # 确保格式正确。
    
    # 但根据报错，似乎是在 ARTICLES 列表定义之后的代码出了问题？
    # "article = next((a for a in ARTICLES if a['slug'    {"
    # 这看起来像是在代码逻辑里插入了字典？？？
    
    # 让我们看看出错的那一行附近
    lines = content.split('\n')
    print(f"总行数: {len(lines)}")
    # 找到报错行附近
    # 但我们最好直接重写整个文件，把那篇导致问题的文章先删掉，恢复正常，然后再想办法正确添加
    
    # 尝试找到最后添加的那个 "json-formatter" 文章并删除它
    clean_lines = []
    skip = False
    for line in lines:
        if '"slug": "json-formatter-online-free-guide"' in line:
            # 这是一个新加的文章开始
            # 我们要回溯删除这一项的开始 '{'
            if clean_lines and clean_lines[-1].strip() == '{':
                clean_lines.pop()
            skip = True
        
        if skip:
            # 如果是 article 的结束 '},'，停止跳过
            if line.strip() == '},' or line.strip() == '}':
                 skip = False
                 continue # 这一行也不要
            continue
        
        clean_lines.append(line)
        
    # 上面的逻辑太复杂且容易错。
    # 让我们手动检查下载下来的文件内容再决定。
    
    ssh.close()

if __name__ == "__main__":
    fix_blog()
