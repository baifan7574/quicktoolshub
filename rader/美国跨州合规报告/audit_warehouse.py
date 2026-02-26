import os
import random
from supabase import create_client

# Load config similar to matrix_reporter.py
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {
        'url': os.getenv('SUPABASE_URL'),
        'key': os.getenv('SUPABASE_KEY')
    }
    
    if not config['url'] or not config['key']:
        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
                    if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
        except:
            pass
    return config

def audit():
    config = load_config()
    if not config['url'] or not config['key']:
        print("CRITICAL ERROR: SUPABASE_URL or SUPABASE_KEY not found.")
        return

    supabase = create_client(config['url'], config['key'])

    # 1. Total Assets
    print("--- 1. WAREHOUSE AUDIT ---")
    try:
        # Total Keywords
        res_total = supabase.table("grich_keywords_pool").select("id", count="exact").execute()
        count_total = res_total.count
        print(f"Total Keywords: {count_total}")

        # Finished Articles
        res_articles = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("final_article", "null").execute()
        count_articles = res_articles.count
        print(f"Finished Articles: {count_articles}")

        # Finished PDFs
        res_pdfs = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("pdf_url", "null").execute()
        count_pdfs = res_pdfs.count
        print(f"Finished PDFs: {count_pdfs}")

        # 2. Quality Check (Random 3)
        print("\n--- 2. QUALITY CHECK (Random 3 PDFs) ---")
        # Get latest 10 and pick 3 to ensure we get recent ones
        res_recent = supabase.table("grich_keywords_pool").select("pdf_url").not_.is_("pdf_url", "null").order("id", desc=True).limit(20).execute()
        
        if res_recent.data:
            samples = random.sample(res_recent.data, min(3, len(res_recent.data)))
            for i, item in enumerate(samples):
                url = item['pdf_url']
                is_valid = "_20260223" in url
                status = "[PASS]" if is_valid else "[FAIL]"
                print(f"Sample {i+1}: {url.split('/')[-1]} -> {status}")
        else:
            print("No PDFs found to sample.")

        # 3. Storage Check
        print("\n--- 3. STORAGE CHECK ---")
        try:
            # List files in bucket to verify access
            res_storage = supabase.storage.from_("audit-reports").list()
            if res_storage:
                print(f"Storage Access: [PASS] (Found {len(res_storage)} files)")
            else:
                 print(f"Storage Access: [PASS] (Bucket empty but accessible)")
        except Exception as e:
            print(f"Storage Access: [FAIL] - {e}")

    except Exception as e:
        print(f"Audit Failed: {e}")

if __name__ == "__main__":
    audit()
