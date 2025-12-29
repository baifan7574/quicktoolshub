import shutil
import os
import time

def restore():
    print("WARNING: This will overwrite your current work with the GOLD STANDARD BACKUP.")
    print("Current State: 2025-12-25 Wish Wall Stable Version")
    confirm = input("Are you sure? (Type 'yes' to confirm): ")
    if confirm != 'yes':
        print("Restoration cancelled.")
        return

    backup_dir = r"d:\quicktoolshub\quicktoolshub-python\_GOLD_STANDARD_BACKUP\2025-12-25_WishWall_Stable"
    target_dir = r"d:\quicktoolshub\quicktoolshub-python"
    
    files_to_restore = [
        ("tools_new.py", "tools_new.py"),
        ("detail_new.html", "detail_new.html"),
        ("deploy_stable.py", "deploy_stable.py"),
        ("blog_final.py", "blog_final.py"),
        ("wish_wall.html", r"templates\pages\wish_wall.html")
    ]

    for src, dest in files_to_restore:
        src_path = os.path.join(backup_dir, src)
        dest_path = os.path.join(target_dir, dest)
        try:
            shutil.copy2(src_path, dest_path)
            print(f"Restored: {dest}")
        except Exception as e:
            print(f"Error restoring {dest}: {e}")

    print("\nFiles restored locally. Now deploying to server to ensure consistency...")
    os.system("python deploy_stable.py")

if __name__ == "__main__":
    restore()
