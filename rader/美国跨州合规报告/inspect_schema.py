import os
import sys
import json
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Missing env vars")
    sys.exit(1)

supabase = create_client(url, key)

def inspect():
    print("--- Inspecting Schema ---")
    try:
        # Get one row to see columns
        res = supabase.table('grich_keywords_pool').select('*').limit(1).execute()
        if res.data:
            print("Columns in grich_keywords_pool:")
            print(json.dumps(list(res.data[0].keys()), indent=2))
        else:
            print("Table empty or access denied")

        # List buckets
        print("\n--- Inspecting Buckets ---")
        res_buckets = supabase.storage.list_buckets()
        print("Buckets found:")
        for b in res_buckets:
            print(f"- {b.name}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
