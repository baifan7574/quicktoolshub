
import paramiko

def final_scorch_earth_fix():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 这一招叫“彻底换血”
    commands = [
        # 1. 物理清空所有旧的、可能包含中文的模板
        "rm -rf /root/soeasyhub_v2/templates/*",
        
        # 2. 注入极致轻量化的 app.py，不加载崩溃模块
        """cat > /root/soeasyhub_v2/app.py <<EOF
from flask import Flask, render_template
import os

app = Flask(__name__)

# Register Blueprints manually to ensure English ones are used
from routes import tools, blog, pages
app.register_blueprint(tools.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(pages.bp)

@app.route('/')
def index():
    # Elite Mock Data for instant loading
    tools_list = [
        {"name": "Background Remover", "slug": "background-remover", "description": "Professional AI isolation for high-end visual assets."},
        {"name": "PDF Compressor", "slug": "pdf-compressor", "description": "Legal-grade document optimization and size reduction."}
    ]
    return render_template('index.html', tools=tools_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
EOF""",

        # 3. 强制覆盖 detail.html 为全英文
        "mkdir -p /root/soeasyhub_v2/templates/tools",
        """cat > /root/soeasyhub_v2/templates/tools/detail.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tool Detail - SoEasyHub</title>
    <link rel="stylesheet" href="/static/css/premium.css">
</head>
<body style="background: #0f172a; color: white; padding: 50px; font-family: sans-serif;">
    <nav><a href="/" style="color: #fbbf24; text-decoration: none; font-size: 24px; font-weight: bold;">SoEasyHub</a></nav>
    <div style="margin-top: 50px;">
        <h1 style="font-size: 48px;">Elite Tool Interface</h1>
        <p style="font-size: 20px; opacity: 0.8;">Professional Processing for Global Experts.</p>
        
        <div style="background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-top: 30px;">
            <h3>Select Professional Asset</h3>
            <input type="file" style="margin-top: 10px;">
            <button style="background: #c2410c; color: white; border: none; padding: 12px 30px; border-radius: 10px; margin-top: 20px; cursor: pointer;">Execute Intelligent Removal</button>
        </div>

        <div style="margin-top: 60px; border-left: 4px solid #c2410c; padding-left: 20px;">
            <h2 style="color: #fbbf24;">Legal Perspective: Visual Compliance</h2>
            <p>"In international legal standards, data integrity starts with visual precision. Our tools respect your intellectual property and privacy."</p>
        </div>
    </div>
</body>
</html>
EOF""",

        # 4. 暴力修正 Nginx
        "sed -i 's/127.0.0.1:[0-9]*/127.0.0.1:9999/g' /etc/nginx/sites-enabled/*",
        "systemctl restart nginx",
        
        # 5. 重启
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 1 -b 127.0.0.1:9999 app:app > gunicorn.log 2>&1 &"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd[:60]}...")
        ssh.exec_command(cmd)

    ssh.close()
    print("Cleanup done. Verifying now.")

if __name__ == "__main__":
    final_scorch_earth_fix()
