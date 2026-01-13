import subprocess
import os
import sys

def sync():
    # Target Root
    root_dir = r"d:\quicktoolshub"
    prefix = "雷达监控。/GRICH"
    remote = "grich-cloud"
    branch = "master"

    print(f"Changing directory to {root_dir}...")
    try:
        os.chdir(root_dir)
    except Exception as e:
        print(f"Failed to change dir: {e}")
        return

    print(f"Pushing subtree {prefix} to {remote} {branch}...")
    # Using shell=True to handle path escaping better if needed, but list is safer
    cmd = ["git", "subtree", "push", "--prefix", prefix, remote, branch]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        if result.returncode == 0:
            print("✅ Sync Successful")
        else:
            print("❌ Sync Failed")
    except Exception as e:
        print(f"Execution Error: {e}")

if __name__ == "__main__":
    sync()
