import os
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {}
    if not os.path.exists(TOKEN_FILE):
        # Fallback absolute path
        abs_path = r"d:\quicktoolshub\rader\美国跨州合规报告\.agent\Token..txt"
        if os.path.exists(abs_path):
            token_path = abs_path
        else:
            print(f"Error: {TOKEN_FILE} not found.")
            return None
    else:
        token_path = TOKEN_FILE
        
    with open(token_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line:
                config['url'] = line.split("Project URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("Secret keys:")[1].strip()
    return config

def main():
    config = load_config()
    if not config: return

    try:
        supabase: Client = create_client(config['url'], config['key'])
        
        # Get total count
        # Supabase-py client uses 'count' parameter in select
        # Select head with count exact
        res = supabase.table("grich_keywords_pool").select("id", count="exact").execute()
        total_count = res.count
        
        print(f"📊 Current Database Stats:")
        print(f"Total Keywords Mined: {total_count}")
        
        # Get Category Breakdown (Note: Group by queries are tricky in simple postgrest, 
        # we might need to fetch all or just report total for now to be fast)
        # Actually proper SQL group by isn't directly supported in basic client select withoutrpc usually,
        # but we can try to fetch separate counts for major categories if needed, or just total for now.
        
        categories = ["Medical", "Law", "Finance", "Education", "RealEstate", "Engineer", "Trades"]
        print("-" * 30)
        print("Category Breakdown (approx):")
        for cat in categories:
            c_res = supabase.table("grich_keywords_pool").select("id", count="exact").eq("category", cat).execute()
            if c_res.count > 0:
                print(f"  - {cat}: {c_res.count}")
                
    except Exception as e:
        print(f"Error querying database: {e}")

if __name__ == "__main__":
    main()
