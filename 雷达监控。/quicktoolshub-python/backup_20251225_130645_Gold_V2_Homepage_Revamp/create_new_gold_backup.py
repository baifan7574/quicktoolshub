import shutil
import os
import datetime

def create_backup():
    # Define source and destination
    source_dir = os.getcwd()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}_Gold_V2_Homepage_Revamp"
    dest_dir = os.path.join(source_dir, backup_name)
    
    print(f"🚀 Starting Gold Standard Backup V2.0...")
    print(f"📂 Source: {source_dir}")
    print(f"📦 Destination: {dest_dir}")
    
    # Ignore patterns
    ignore_patterns = shutil.ignore_patterns(
        '__pycache__', '*.pyc', '.git', '.vscode', 'venv', 'env', 
        'backup_*', '_GOLD_STANDARD_BACKUP*' # Don't backup inside other backups
    )
    
    try:
        shutil.copytree(source_dir, dest_dir, ignore=ignore_patterns)
        print(f"\n✅ Backup Complete Successfully!")
        print(f"🏆 This directory is now the GOLD STANDARD for restoration.")
        return dest_dir
    except Exception as e:
        print(f"\n❌ Backup Failed: {e}")
        return None

if __name__ == "__main__":
    create_backup()
