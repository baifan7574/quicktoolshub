import os
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")
BUCKET = "raw-handbooks"

def load_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line:
                config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("keys:")[1].strip()
    return config

def main():
    config = load_config()
    supabase: Client = create_client(config['url'], config['key'])
    
    print("🧹 Cleaning Dirty Data (Aligning DB with Storage)...")
    
    # 1. Get Physical Files
    print(f"   📂 Listing storage files in '{BUCKET}'...")
    storage_files = set()
    try:
        files = supabase.storage.from_(BUCKET).list()
        for f in files:
            storage_files.add(f['name'])
        print(f"   ✅ Found {len(storage_files)} physical files.")
    except Exception as e:
        print(f"   ❌ Failed to list storage: {e}")
        return

    # 2. Get DB Records marked as downloaded
    print("   📊 Fetching 'is_downloaded=True' records...")
    try:
        # Fetching all might be large, but for now 29 is small
        res = supabase.table("grich_keywords_pool").select("*").eq("is_downloaded", True).execute()
        db_records = res.data
        print(f"   🧐 Found {len(db_records)} records marked as downloaded.")
    except Exception as e:
        print(f"   ❌ Failed to query DB: {e}")
        return

    # 3. Compare and Rollback
    for record in db_records:
        slug = record['slug']
        expected_filename = f"{slug}.pdf"
        
        if expected_filename not in storage_files:
            # DIRTY DATA DETECTED
            print(f"   ⚠️ MISMATCH: {slug} (No Physical File) -> Resetting to PENDING...")
            try:
                supabase.table("grich_keywords_pool").update({
                    "is_downloaded": False,
                    "state": "pending_retry" # Reset state so it gets picked up
                }).eq("id", record['id']).execute()
            except Exception as e:
                print(f"      ❌ Update failed: {e}")
        else:
            print(f"   ✅ VERIFIED: {slug} exists.")

    print("\n✨ Data Cleaned. Ready for re-run.")

if __name__ == "__main__":
    main()
