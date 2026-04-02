import os
from supabase import create_client, Client

# Environment variable names for cloud deployment
ENV_SUPABASE_URL = "SUPABASE_URL"
ENV_SUPABASE_KEY = "SUPABASE_KEY"

def get_supabase_client():
    config = {}
    
    # Priority 1: Read from environment variables (cloud deployment)
    supabase_url = os.environ.get(ENV_SUPABASE_URL)
    supabase_key = os.environ.get(ENV_SUPABASE_KEY)
    
    if supabase_url and supabase_key:
        config['url'] = supabase_url
        config['key'] = supabase_key
        return create_client(config['url'], config['key'])
    
    # Priority 2: Fallback to local Token file (development)
    token_path = os.path.join(".agent", "Token..txt")
    if not os.path.exists(token_path):
        # Try alternative relative path
        token_path = os.path.join("doc", "Token..txt")
    
    if os.path.exists(token_path):
        with open(token_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if "Project URL:" in line:
                    config['url'] = line.split("URL:")[1].strip()
                if "Secret keys:" in line:
                    config['key'] = line.split("keys:")[1].strip()
        return create_client(config['url'], config['key'])
    
    print("Could not load Supabase config.")
    return None

def check_status():
    supabase = get_supabase_client()
    if not supabase:
        return

    print("--- PIPELINE STATUS REPORT ---")

    # 1. Check Total Keywords
    res_total = supabase.table("grich_keywords_pool").select("id", count="exact").execute()
    total_count = res_total.count
    print(f"Total Keywords in Pool: {total_count}")

    # 2. Check Librarian Progress (is_downloaded = True)
    res_downloaded = supabase.table("grich_keywords_pool").select("id", count="exact").eq("is_downloaded", True).execute()
    downloaded_count = res_downloaded.count
    print(f"Librarian Downloaded (is_downloaded=True): {downloaded_count}")

    # 3. Check Composer Progress (final_article != null)
    res_composed = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("final_article", "null").execute()
    composed_count = res_composed.count
    print(f"Composer Finished (final_article!=null): {composed_count}")

    # 4. Check Reporter Progress (pdf_url != null)
    res_reported = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("pdf_url", "null").execute()
    reported_count = res_reported.count
    print(f"Reporter Finished (pdf_url!=null): {reported_count}")

    print("\n--- TARGET VERIFICATION ---")
    if reported_count >= 324:
        print("✅ SUCCESS: Reporter count has reached target (>= 324)!")
    else:
        print(f"⚠️ PENDING: Reporter count is {reported_count}. Waiting for pipeline...")

if __name__ == "__main__":
    check_status()
