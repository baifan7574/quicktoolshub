import os
import shutil
import subprocess
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

REPO_URL = "https://github.com/baifan7574/grich-cloud.git"
WORK_DIR = r"d:\quicktoolshub\雷达监控。\GRICH"
TEMP_DIR = os.path.join(WORK_DIR, "temp_deploy")

def run(cmd, cwd=None):
    print(f"Exec: {cmd}")
    subprocess.run(cmd, cwd=cwd, check=True, shell=True)

def main():
    if os.path.exists(TEMP_DIR):
        print("Cleaning old temp dir...")
        # Use shell command to remove avoid python permissions issues
        subprocess.run(f"rmdir /s /q \"{TEMP_DIR}\"", shell=True)
    
    print(f"Cloning {REPO_URL}...")
    run(f"git clone {REPO_URL} \"{TEMP_DIR}\"")

    print("Copying files...")
    excluded_dirs = {'.git', 'node_modules', '.next', 'temp_deploy', 'dist', 'build', '.vscode'}
    
    for root, dirs, files in os.walk(WORK_DIR):
        # Modify dirs in-place to exclude unwanted
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        # Also skip if we are somehow inside excluded dir (safety)
        if any(ex in root for ex in excluded_dirs):
            continue

        rel_path = os.path.relpath(root, WORK_DIR)
        
        # Don't copy root files if they are not part of repo structure? 
        # Checking file list: GRICH contains AWS...txt and folders.
        # We copy everything.
        
        target_path = os.path.join(TEMP_DIR, rel_path)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            
        for file in files:
            # Skip specific files
            if file == 'deploy_to_repo.py' or file.endswith('.pem') or file == 'sync_repo.py':
                continue
                
            src = os.path.join(root, file)
            dst = os.path.join(target_path, file)
            try:
                shutil.copy2(src, dst)
            except Exception as e:
                print(f"Failed to copy {file}: {e}")

    print("Pushing changes...")
    try:
        run("git add .", cwd=TEMP_DIR)
        # Check status
        status = subprocess.run("git status --porcelain", cwd=TEMP_DIR, capture_output=True, text=True)
        if not status.stdout.strip():
            print("No changes to commit.")
        else:
            run('git commit -m "Auto-deploy: Sync from quicktoolshub local"', cwd=TEMP_DIR)
            run("git push", cwd=TEMP_DIR)
            print("✅ Success! Deployed to grich-cloud.")
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
