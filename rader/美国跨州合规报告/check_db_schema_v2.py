import os
import sys
import json
from supabase import create_client

def check_schema():
    # Load credentials from .agent/Token..txt since we are local and env vars might not be set in this shell
    try:
        with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
            content = f.read()
            url = None
            key = None
            for line in content.split('\n'):
                if 'Project URL:' in line:
                    url = line.split('Project URL:')[1].strip()
                if 'Secret keys:' in line:
                    key = line.split('Secret keys:')[1].strip()
    except Exception as e:
        print(f"Error reading token file: {e}")
        return

    if not url or not key:
        print("Could not find credentials")
        return

    print(f"Connecting to {url}")
    supabase = create_client(url, key)

    try:
        # Fetch one record to see all columns
        res = supabase.table("grich_keywords_pool").select("*").limit(1).execute()
        if res.data:
            print("Columns found:")
            print(json.dumps(list(res.data[0].keys()), indent=2))
            print("\nSample Data:")
            print(json.dumps(res.data[0], indent=2))
        else:
            print("No data found in table")
    except Exception as e:
        print(f"Error querying Supabase: {e}")

if __name__ == "__main__":
    check_schema()
