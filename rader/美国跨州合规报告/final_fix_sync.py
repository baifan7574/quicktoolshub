import os
import subprocess
from datetime import datetime

REPO_URL = "https://github.com/baifan7574/soeasyhub-v2-main.git"

def run_cmd(cmd, cwd=None):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")
    return result

def main():
    print("🚀 Initiating Absolute Final Sync for soeasyhub-v2...")
    cwd = "soeasyhub-v2"
    
    # 1. Config
    run_cmd('git config user.name "MatrixAgent"', cwd=cwd)
    run_cmd('git config user.email "agent@soeasyhub.com"', cwd=cwd)
    
    # 2. Sync all branches
    run_cmd("git add .", cwd=cwd)
    run_cmd('git commit -m "Fix: Worker loop and sync sync"', cwd=cwd)
    
    print("📢 Pushing to MAIN and MASTER...")
    run_cmd("git push origin main:main --force", cwd=cwd)
    run_cmd("git push origin main:master --force", cwd=cwd)
    
    # 3. Cloudflare Deploy (Fixing the 1101)
    print("🌐 Deploying Worker Fix to Cloudflare...")
    cf_env = os.environ.copy()
    cf_env["CLOUDFLARE_EMAIL"] = "baifan7574@gmail.com"
    cf_env["CLOUDFLARE_API_KEY"] = "69e5dc3505d1f288a82f23d5c1b8899756fae"
    
    # Using specific name and compatibility date to be safe
    deploy_cmd = "npx wrangler deploy --name soeasyhub-v2 --compatibility-date 2024-04-03"
    res = subprocess.run(deploy_cmd, shell=True, cwd=cwd, env=cf_env, capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Cloudflare Worker Refreshed.")
    else:
        print(f"❌ Worker Deploy Failed: {res.stderr}")

if __name__ == "__main__":
    main()
