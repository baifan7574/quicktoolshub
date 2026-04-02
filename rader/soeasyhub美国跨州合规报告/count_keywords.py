import os
from supabase import create_client

TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {
        'url': os.getenv('SUPABASE_URL'),
        'key': os.getenv('SUPABASE_KEY'),
    }
    if not config['url'] or not config['key']:
        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if "Project URL:" in line: 
                        config['url'] = line.split("URL:")[1].strip()
                    if "Secret keys:" in line: 
                        config['key'] = line.split("keys:")[1].strip()
        except Exception as e:
            print(f"Error loading config: {e}")
            pass
    return config

def main():
    config = load_config()
    if not config['url'] or not config['key']:
        print("Error: Supabase URL or Key not found.")
        return

    try:
        supabase = create_client(config['url'], config['key'])
        
        print("Querying database for keyword count...")
        
        # Method 1: select count with head=True (most efficient for just count)
        res = supabase.table("grich_keywords_pool").select("*", count="exact", head=True).execute()
        
        if res.count is not None:
            print(f"Total keywords in 'grich_keywords_pool': {res.count}")
        else:
            print("Could not retrieve count.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
