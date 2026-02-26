import os
import subprocess

REPO_URL = "https://github.com/baifan7574/soeasyhub-v2-main.git"

def run_cmd(cmd, cwd=None):
    print(f"Executing: {cmd}")
    # Using list for subprocess to avoid shell quoting issues
    import shlex
    if isinstance(cmd, str):
        cmd_list = shlex.split(cmd) if os.name != 'nt' else cmd
    else:
        cmd_list = cmd
    
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")
    return result

def main():
    print("[DEPLOY] Initiating Final Git Sync for soeasyhub-v2...")
    
    # Init if not already
    if not os.path.exists("soeasyhub-v2/.git"):
        run_cmd("git init -b main", cwd="soeasyhub-v2") # Try to force main
    
    # Configure user if not set
    run_cmd('git config user.name "MatrixAgent"', cwd="soeasyhub-v2")
    run_cmd('git config user.email "agent@soeasyhub.com"', cwd="soeasyhub-v2")

    # Add Remote
    run_cmd(f"git remote add origin {REPO_URL}", cwd="soeasyhub-v2")
    
    # Add all files
    run_cmd("git add .", cwd="soeasyhub-v2")
    
    # Simple commit
    run_cmd('git commit -m "AutoDeploymentV2"', cwd="soeasyhub-v2")
    
    # Push
    print("[PUSH] Attempting to push to remote...")
    # Check current branch
    res = subprocess.run("git branch --show-current", shell=True, cwd="soeasyhub-v2", capture_output=True, text=True)
    branch = res.stdout.strip() or "master"
    print(f"Current branch: {branch}")
    
    run_cmd(f"git push -u origin {branch}:main --force", cwd="soeasyhub-v2")

if __name__ == "__main__":
    main()
