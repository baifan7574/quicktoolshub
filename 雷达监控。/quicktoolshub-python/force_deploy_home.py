import paramiko
import os

def deploy_new_home():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    # 重新设计的 index.html 模板内容 - 针对 Flask 环境
    new_index_content = """{% extends "base.html" %}

{% block content %}
<div class="hero-section" style="padding: 60px 0; background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%);">
    <div class="container text-center">
        <h1 class="hero-title playfair" style="font-size: 3.5rem; color: #1e293b; margin-bottom: 10px;">SoEasyHub</h1>
        <h2 class="hero-slogan playfair italic" style="font-size: 1.5rem; color: #475569; margin-bottom: 20px;">Free Online Tools: Secure, Private & 100% Free</h2>
        <p class="hero-description Outfit" style="max-width: 700px; margin: 0 auto 30px; font-size: 1.1rem; color: #64748b; line-height: 1.6;">
            Professional tools for PDF, Image, and Text. <br>
            <strong>No Watermarks, No Registration, Processes 100% in your browser.</strong>
        </p>
        
        <div style="max-width: 600px; margin: 0 auto 40px; position: relative;">
            <form action="/search" method="get" style="position: relative;">
                <input type="text" name="q" placeholder="What tool do you need? (e.g. PDF Compressor)" 
                       style="width: 100%; padding: 15px 20px 15px 50px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1.1rem; outline: none; transition: border-color 0.2s;">
                <span style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); font-size: 1.2rem;">🔍</span>
            </form>
        </div>
    </div>
</div>

<section class="tools-grid-section container" style="padding: 60px 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
        <h3 class="section-label Outfit" style="font-size: 1.8rem; font-weight: 700; margin: 0;">🚀 Top Performance Tools</h3>
        <a href="/tools" style="color: #2563eb; font-weight: 600; text-decoration: none;">View All Tools →</a>
    </div>
    
    <div class="tools-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
        <!-- PDF Compressor -->
        <a href="/tools/pdf-compressor" style="text-decoration: none; color: inherit; display: block;">
            <div class="tool-card-premium shadow-sm" style="padding: 30px; border-radius: 20px; background: #fff; border: 1px solid #f1f5f9; transition: all 0.3s; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 20px;">📄</div>
                <h4 class="tool-name playfair" style="font-size: 1.4rem; font-weight: 700; margin-bottom: 10px;">PDF Compressor</h4>
                <p class="tool-desc Outfit" style="color: #64748b; line-height: 1.5; font-size: 1rem;">Reduce PDF file size without losing quality. Your files never leave your computer.</p>
                <div style="margin-top: 15px; color: #2563eb; font-weight: 600; font-size: 0.9rem;">Use Tool →</div>
            </div>
        </a>

        <!-- Image Resizer -->
        <a href="/tools/image-resizer" style="text-decoration: none; color: inherit; display: block;">
            <div class="tool-card-premium shadow-sm" style="padding: 30px; border-radius: 20px; background: #fff; border: 1px solid #f1f5f9; transition: all 0.3s; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 20px;">🖼️</div>
                <h4 class="tool-name playfair" style="font-size: 1.4rem; font-weight: 700; margin-bottom: 10px;">Image Resizer</h4>
                <p class="tool-desc Outfit" style="color: #64748b; line-height: 1.5; font-size: 1rem;">Resize JPG, PNG & WebP images locally. High quality and super fast.</p>
                <div style="margin-top: 15px; color: #2563eb; font-weight: 600; font-size: 0.9rem;">Use Tool →</div>
            </div>
        </a>

        <!-- Background Remover -->
        <a href="/tools/background-remover" style="text-decoration: none; color: inherit; display: block;">
            <div class="tool-card-premium shadow-sm" style="padding: 30px; border-radius: 20px; background: #fff; border: 1px solid #f1f5f9; transition: all 0.3s; height: 100%;">
                <div style="font-size: 3rem; margin-bottom: 20px;">✨</div>
                <h4 class="tool-name playfair" style="font-size: 1.4rem; font-weight: 700; margin-bottom: 10px;">Background Remover</h4>
                <p class="tool-desc Outfit" style="color: #64748b; line-height: 1.5; font-size: 1rem;">Remove backgrounds from images instantly using local AI. 100% Private.</p>
                <div style="margin-top: 15px; color: #2563eb; font-weight: 600; font-size: 0.9rem;">Use Tool →</div>
            </div>
        </a>
    </div>
</section>

<section style="background: #f8faff; padding: 60px 0; border-top: 1px solid #e2e8f0;">
    <div class="container">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 15px;">🔒</div>
                <h3 style="font-weight: 700; margin-bottom: 10px;">Privacy First</h3>
                <p style="color: #64748b; font-size: 0.95rem;">Processing happens in your browser. No data is sent to our servers.</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 15px;">⚡</div>
                <h3 style="font-weight: 700; margin-bottom: 10px;">Fast & Easy</h3>
                <p style="color: #64748b; font-size: 0.95rem;">Optimized tools designed to get your task done in seconds.</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 15px;">💰</div>
                <h3 style="font-weight: 700; margin-bottom: 10px;">Always Free</h3>
                <p style="color: #64748b; font-size: 0.95rem;">No subscriptions, no watermarks, no hidden costs. Truly free.</p>
            </div>
        </div>
    </div>
</section>

<style>
    .tool-card-premium:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #2563eb !important;
    }
</style>
{% endblock %}
"""
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname, username=username, password=password)
        print("✅ 已连接服务器，准备执行手术...")
        
        # 备份旧页面
        ssh.exec_command("cp /root/soeasyhub_v2/templates/index.html /root/soeasyhub_v2/templates/index.html.bak")
        
        # 写入新页面 (使用 SFTP 确保编码正确)
        sftp = ssh.open_sftp()
        with sftp.file('/root/soeasyhub_v2/templates/index.html', 'w') as f:
            f.write(new_index_content)
        sftp.close()
        
        print("✅ 首页模板已更新为「黄金入口版」")
        
        # 重启 Flask (gunicorn)
        print("🔄 正在强制重启服务以刷新缓存...")
        ssh.exec_command("pkill -HUP gunicorn")
        
        print("\n" + "="*50)
        print("🚀 首页改版已全网生效！")
        print("="*50)
        print("1. 剔除了高冷文案")
        print("2. 注入了「免费/隐私/无水印」SEO关键词")
        print("3. 把最赚钱的三个工具放到了最显眼位置")
        print("="*50)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_new_home()
