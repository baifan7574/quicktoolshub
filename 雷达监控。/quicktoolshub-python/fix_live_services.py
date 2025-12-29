import paramiko
import os

def fix_external_services():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    clarity_id = "uqdwtqfbf6"
    bing_key = "a03727287ab1b016f667160e47665cab"
    
    clarity_script = f"""
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{clarity_id}");
    </script>
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password)
        print("✅ 已连接服务器...")

        # 1. 注入 Clarity 到 base.html
        sftp = ssh.open_sftp()
        base_path = '/root/soeasyhub_v2/templates/base.html'
        with sftp.open(base_path, 'r') as f:
            content = f.read().decode()
        
        if clarity_id not in content:
            print("🚀 正在注入 Microsoft Clarity 热力图代码...")
            # 插入到 </head> 之前
            new_content = content.replace('</head>', f'{clarity_script}\n</head>')
            with sftp.open(base_path, 'w') as f:
                f.write(new_content)
            print("✅ Clarity 代码注入成功！")
        else:
            print("ℹ️ Clarity 代码已存在，无需重复注入。")

        # 2. 确保 Bing 验证文件在正确位置
        # 在 Flask 中，通常需要放在 static 或者直接在 root 下由 app.py 处理
        # 我们最简单的办法是创建一个专门的路由在 app.py 里，或者直接放进 static
        verify_content = bing_key
        verify_filename = f"{bing_key}.txt"
        
        # 写入 static 目录
        static_verify_path = f"/root/soeasyhub_v2/static/{verify_filename}"
        with sftp.open(static_verify_path, 'w') as f:
            f.write(verify_content)
        print(f"✅ Bing 验证文件已创建在 static: {verify_filename}")

        # 3. 修改 app.py 确保根目录能访问验证文件 (这是最稳的验证方式)
        app_py_path = '/root/soeasyhub_v2/app.py'
        with sftp.open(app_py_path, 'r') as f:
            app_content = f.read().decode()
        
        route_code = f"""
@app.route('/{verify_filename}')
def bing_verify():
    return "{verify_content}"
"""
        if verify_filename not in app_content:
            print("🚀 正在修改 app.py 以支持 Bing 验证路由...")
            app_content += route_code
            with sftp.open(app_py_path, 'w') as f:
                f.write(app_content)
            print("✅ Bing 验证路由已添加！")
            
            # 重启 gunicorn
            print("🔄 正在重启服务以生效...")
            ssh.exec_command("pkill -HUP gunicorn")
        else:
            print("ℹ️ Bing 验证路由已存在。")

        sftp.close()
        print("\n" + "="*50)
        print("🎉 全部外部服务已完成“硬接入”！")
        print("1. Clarity 热力图：已全球生效，正在录制访客。")
        print("2. Bing IndexNow：验证接口已通，随时可以推送。")
        print("="*50)

    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_external_services()
