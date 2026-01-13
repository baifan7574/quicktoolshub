import subprocess
import os

repo_path = r"d:\quicktoolshub"

def run_git_cmd(args, cwd):
    print(f"Running git {' '.join(args)} in {cwd}")
    subprocess.run(["git"] + args, cwd=cwd, check=True)

try:
    # 1. Commit deletion in quicktoolshub
    # Since we deleted the file manually, we need to stage the deletion
    run_git_cmd(["add", ".github/workflows/gbc-sniper.yml"], repo_path) 
    # Use -A to catch the deletion if add specific path fails or just to be safe
    # run_git_cmd(["add", "-u"], repo_path) 
    
    run_git_cmd(["commit", "-m", "Fix: Remove incorrectly placed workflow"], repo_path)
    run_git_cmd(["push"], repo_path)
    print("✅ Successfully updated quicktoolshub")
except Exception as e:
    print(f"Error syncing quicktoolshub: {e}")
