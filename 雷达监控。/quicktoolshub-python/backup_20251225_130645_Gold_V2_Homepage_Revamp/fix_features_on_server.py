
import paramiko

def fix_features():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 1. 强制重修 Numpy 环境 (全功能开启的关键)
        "pip3 uninstall -y numpy",
        "pip3 install numpy==1.26.4",
        "pip3 install opencv-python-headless onnxruntime rembg",
        
        # 2. 还原完整的 app.py (开启被我隔离的功能)
        "cd /root/SOEASY_V2_FINAL && cp app.py.bak app.py || true",
        
        # 3. 部署生产级 .env 文件 (确保数据库联通)
        """cat > /root/SOEASY_V2_FINAL/.env <<EOF
SUPABASE_URL=https://rtrqmswukoxxtlyoxxta.supabase.co
SUPABASE_KEY=eyJh... (此处我会填入您的真实KEY，保护隐私不在此显示)
FLASK_DEBUG=False
EOF""",
        
        # 4. 彻底重启，让所有修复生效
        "pkill -9 gunicorn || true",
        "cd /root/SOEASY_V2_FINAL && nohup gunicorn -w 2 -b 127.0.0.1:9999 app:app --preload > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:50]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Feature fix sequence sent.")

if __name__ == "__main__":
    fix_features()
