import subprocess
import os

repo_path = r"d:\quicktoolshub\雷达监控。\GRICH\grich-astro"

def run_git_cmd(args, cwd):
    print(f"Running git {' '.join(args)} in {cwd}")
    subprocess.run(["git"] + args, cwd=cwd, check=True)

try:
    run_git_cmd(["add", ".github/workflows/gbc-sniper.yml"], repo_path) 
    run_git_cmd(["commit", "-m", "Feat: Activate Engine 2 Sniper Automation"], repo_path)
    run_git_cmd(["push"], repo_path)
    print("✅ Successfully activated Engine 2 in grich-cloud")
except Exception as e:
    print(f"Error syncing grich-cloud: {e}")
