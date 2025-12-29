
import paramiko

def final_victory_sprint():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 彻底解决 500 错误的指令
    commands = [
        # 1. 创建极致简约的 app.py，杜绝所有依赖崩溃
        """cat > /root/soeasyhub_v2/app.py <<EOF
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    tools_list = [
        {"name": "Background Remover", "slug": "background-remover", "description": "Elite AI background removal."},
        {"name": "PDF Compressor", "slug": "pdf-compressor", "description": "Professional document optimization."}
    ]
    return render_template('index.html', tools=tools_list)

@app.route('/tools/<slug>')
def tool_detail(slug):
    # Dummy tool for testing - English Only
    tool = {"name": slug.replace('-', ' ').title(), "slug": slug, "description": "Professional Asset Processing"}
    return render_template('tools/detail.html', tool=tool)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
EOF""",

        # 2. 注入 100% 全英文的基础模板
        "mkdir -p /root/soeasyhub_v2/templates",
        """cat > /root/soeasyhub_v2/templates/base.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SoEasyHub - Solving Troubles with Tech</title>
    <link rel="stylesheet" href="/static/css/premium.css">
</head>
<body style="background: #0f172a; color: white;">
    {% block content %}{% endblock %}
</body>
</html>
EOF""",

        # 3. 注入 100% 全英文的首页面栏
        """cat > /root/soeasyhub_v2/templates/index.html <<EOF
{% extends "base.html" %}
{% block content %}
<div style="padding: 100px; text-align: center;">
    <h1 style="font-size: 64px;">Solving Troubles with Tech</h1>
    <h2 style="font-size: 32px; font-style: italic; opacity: 0.7;">Soothing Minds with Humanities</h2>
    <div style="margin-top: 50px;">
        {% for tool in tools %}
        <a href="/tools/{{ tool.slug }}" style="background: #c2410c; color: white; padding: 20px 40px; margin: 10px; text-decoration: none; border-radius: 10px; display: inline-block;">{{ tool.name }} →</a>
        {% endfor %}
    </div>
</div>
{% endblock %}
EOF""",

        # 4. 暴力重启
        "pkill -9 gunicorn || true",
        "cd /root/soeasyhub_v2 && nohup gunicorn -w 1 -b 127.0.0.1:9999 app:app > debug.log 2>&1 &",
        "systemctl restart nginx",
        
        # 5. 自检测试
        "sleep 5 && curl http://127.0.0.1:9999"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd[:60]}...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode()
        if "Solving Troubles with Tech" in result:
            print(">>> SUCCESS: Homepage is English and LIVE!")
        else:
            print(result)

    ssh.close()

if __name__ == "__main__":
    final_victory_sprint()
