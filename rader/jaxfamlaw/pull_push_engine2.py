import subprocess
import os

repo_path = r"d:\quicktoolshub\雷达监控。\GRICH\grich-astro"

def run_git_cmd(args, cwd):
    print(f"Running git {' '.join(args)} in {cwd}")
    subprocess.run(["git"] + args, cwd=cwd, check=True)

try:
    print("🔄 Pulling latest changes from remote...")
    run_git_cmd(["pull", "--rebase", "origin", "main"], repo_path) 
    print("🚀 Pushing Engine 2 activation...")
    run_git_cmd(["push", "origin", "main"], repo_path)
    print("✅ Successfully activated Engine 2 in grich-cloud")
except Exception as e:
    print(f"Error syncing grich-cloud: {e}")
