"""
修复 detail.html - 删除旧的 Image Compressor SEO 内容，只保留新的优化版本
"""
import paramiko
from scp import SCPClient
import time

def fix_detail_html():
    print("=" * 80)
    print("修复 detail.html - 删除重复的 SEO 内容")
    print("=" * 80)
    
    # 读取文件
    print("\n读取 detail.html...")
    with open('templates/tools/detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到并删除旧的 Image Compressor SEO 部分 (从 441 行开始的那个)
    old_section_start = '''        {% elif 'compress' in tool.slug and 'image' in tool.slug %}
        <div class="expert-section">
            <div class="scary-seo-content">
                <h2 class="playfair">Digital Presence: Why Image Size Destroys First Impressions</h2>'''
    
    old_section_end = '''        </div>


        <h3>📚 Learn More</h3>'''
    
    # 删除旧内容
    start_pos = content.find(old_section_start)
    end_pos = content.find(old_section_end)
    
    if start_pos != -1 and end_pos != -1:
        # 删除旧的 SEO 部分
        content = content[:start_pos] + content[end_pos:]
        print("✅ 已删除旧的 Image Compressor SEO 内容")
    else:
        print("⚠️ 未找到旧内容，可能已被删除")
    
    # 保存
    with open('templates/tools/detail.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ detail.html 已修复")
    
    # 部署到服务器
    print("\n部署到服务器...")
    
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
        
        print("\n重启服务...")
        ssh.exec_command("pkill -9 gunicorn || true")
        time.sleep(3)
        ssh.exec_command("cd /root/soeasyhub_v2 && nohup gunicorn -w 2 --timeout 300 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &")
        time.sleep(3)
        
        # 验证服务启动
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        ps_output = stdout.read().decode()
        
        if ps_output:
            print("✅ 服务已启动")
        else:
            print("❌ 服务启动失败")
        
        print("\n" + "=" * 80)
        print("✅ 修复完成！")
        print("=" * 80)
        
        print("\n现在 Image Compressor 页面只有一套 SEO 内容：")
        print("  ✅ How to Compress Images Without Losing Quality")
        print("  ✅ 包含所有优化的关键词")
        print("  ✅ 页面更简洁、更专业")
        
        print("\n请访问查看：")
        print("  • http://soeasyhub.com/tools/image-compressor")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_detail_html()
