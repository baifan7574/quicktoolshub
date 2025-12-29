#!/usr/bin/env python3
"""
部署前强制检查脚本
必须全部通过才允许部署
"""
import subprocess
import paramiko
import sys

def check_local_syntax():
    """检查本地文件语法"""
    print("🔍 检查本地语法...")
    files = ['tools_new.py', 'blog_final.py']
    
    for f in files:
        result = subprocess.run(['python', '-m', 'py_compile', f], 
                              capture_output=True)
        if result.returncode != 0:
            print(f"❌ {f} 语法错误:")
            print(result.stderr.decode())
            return False
        print(f"✓ {f} 语法正确")
    
    return True

def check_nginx_port():
    """检查Nginx配置端口"""
    print("\n🔍 检查Nginx端口配置...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('43.130.229.184', username='root', password='baifan100100')
    
    _, stdout, _ = ssh.exec_command('grep proxy_pass /etc/nginx/sites-enabled/*')
    result = stdout.read().decode()
    
    if '9999' in result:
        print("✓ Nginx 配置端口: 9999")
        ssh.close()
        return 9999
    elif '3000' in result:
        print("⚠️  Nginx 配置端口: 3000")
        ssh.close()
        return 3000
    else:
        print("❌ 无法确定Nginx端口")
        ssh.close()
        return None

def check_pm2():
    """检查PM2进程"""
    print("\n🔍 检查PM2进程...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('43.130.229.184', username='root', password='baifan100100')
    
    _, stdout, _ = ssh.exec_command('pm2 list')
    result = stdout.read().decode()
    
    if 'online' in result:
        print("⚠️  警告: 发现运行中的PM2进程")
        print("   部署时需要先停止PM2")
        ssh.close()
        return True  # 返回True表示有PM2
    else:
        print("✓ 没有PM2进程冲突")
        ssh.close()
        return False

def check_deployment_script():
    """检查部署脚本端口配置"""
    print("\n🔍 检查部署脚本...")
    
    with open('deploy_full.py', 'r') as f:
        content = f.read()
    
    if '127.0.0.1:9999' in content:
        print("✓ 部署脚本使用正确端口: 9999")
        return True
    elif '0.0.0.0:3000' in content or 'localhost:3000' in content:
        print("❌ 部署脚本使用错误端口: 3000")
        return False
    else:
        print("⚠️  无法确定部署脚本端口")
        return None

def main():
    print("=" * 60)
    print("  部署前强制检查")
    print("=" * 60)
    
    all_passed = True
    
    # 检查1: 本地语法
    if not check_local_syntax():
        all_passed = False
    
    # 检查2: Nginx端口
    nginx_port = check_nginx_port()
    if nginx_port != 9999:
        print("⚠️  警告: Nginx端口不是标准的9999")
        all_passed = False
    
    # 检查3: PM2
    has_pm2 = check_pm2()
    # PM2存在不算失败,只是警告
    
    # 检查4: 部署脚本
    if not check_deployment_script():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有检查通过,可以部署")
        print("=" * 60)
        return 0
    else:
        print("❌ 检查未通过,请修复后再部署")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
