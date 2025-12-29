import os
import shutil
import subprocess

# SoEasyHub Emergency Rollback System
# Restores the "Gold Standard" from stable_nexus to the live server

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STABLE_DIR = os.path.join(BASE_DIR, "stable_nexus", "latest_working")

def rollback():
    print("🚀 Starting Emergency Rollback to Gold Standard...")
    
    # 1. Verification
    if not os.path.exists(STABLE_DIR):
        print(f"❌ Error: Stable backup not found at {STABLE_DIR}")
        return

    # 2. Local Restoration (Overwrite development files with safe versions)
    file_mapping = {
        "app.py": "app.py",
        "tools_new.py": "tools_new.py",
        "blog_final.py": "blog_final.py",
        "detail_new.html": "detail_new.html",
        "api.py": os.path.join("routes", "api.py"),
        "index.html": os.path.join("templates", "index.html")
    }

    for stable_name, local_path in file_mapping.items():
        src = os.path.join(STABLE_DIR, stable_name)
        dst = os.path.join(BASE_DIR, local_path)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ Restored local: {local_path}")
        else:
            print(f"⚠️ Warning: Backup file {stable_name} missing from stable nexus.")

    # 3. Force Deployment
    print("\n📦 Pushing Gold Standard to server...")
    try:
        # We use the verified deployment script
        result = subprocess.run(["python", "force_deploy_verified.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✨ SUCCESS: Site has been rolled back to the last known stable state.")
        else:
            print("❌ Deployment Failed during rollback.")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error executing deployment script: {e}")

if __name__ == "__main__":
    rollback()
