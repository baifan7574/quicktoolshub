import os
import sys

def fix_paths():
    """
    解决由于 Windows 路径编码（如 '雷达监控。'）和 Python 环境差异导致的部署工具链失效问题。
    """
    print("🛠️  正在启动部署工具链路径修复程序...")
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"📍 当前目录: {current_dir}")
    
    # 查找关键文件
    found_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file in ['deploy_all.bat', 'deploy_pages.py', 'deploy_to_repo.py']:
                found_files.append(os.path.join(root, file))
    
    if not found_files:
        print("❌ 未在当前目录及子目录中找到部署脚本。")
        print("👉 请确保您在项目的根目录运行此脚本。")
        return

    for script_path in found_files:
        print(f"🔍 检查脚本: {script_path}")
        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 自动识别并替换过时的绝对路径
            # 替换 d:\quicktoolshub\雷达监控。\GRICH 等类似路径为当前实际路径
            new_content = content
            
            # 修复常见的硬编码路径模式
            if 'd:\\quicktoolshub' in new_content.lower():
                print(f"   ⚠️  发现硬编码路径，正在转换为相对路径或当前环境路径...")
                # 尝试将旧路径替换为相对于当前脚本位置的路径
                # 这里我们采取更稳健的策略：提示用户手动确认，或者自动替换为变量
                # 针对本项目，我们将路径统一指向当前 workspace 下的 grich-astro
                astro_path = os.path.join(current_dir, 'grich-astro').replace('\\', '\\\\')
                # 这里的正则匹配需要非常小心
                import re
                new_content = re.sub(r'[a-zA-Z]:\\quicktoolshub\\[^\\]+\\GRICH', current_dir.replace('\\', '\\\\'), new_content, flags=re.IGNORECASE)
                new_content = re.sub(r'[a-zA-Z]:\\quicktoolshub\\rader\\jaxfamlaw', current_dir.replace('\\', '\\\\'), new_content, flags=re.IGNORECASE)

            if new_content != content:
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"   ✅ 已修复路径引用。")
            else:
                print(f"   👌 脚本路径看起来是正常的。")
                
        except Exception as e:
            print(f"   ❌ 处理脚本时出错: {e}")

    print("\n🚀 建议操作:")
    print("1. 请尝试直接在命令行运行: python deploy_to_repo.py")
    print("2. 如果依然提示路径找不到，请检查您的 .env 文件是否包含了正确的路径配置。")
    print("3. Cloudflare Pages 部署失败通常是因为 build.js 没复制 functions 文件夹，我已在计划中修复。")

if __name__ == "__main__":
    fix_paths()
