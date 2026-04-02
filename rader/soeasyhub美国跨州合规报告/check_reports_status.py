import sys
import os
import io
import json

# Fix stdout encoding for Windows to avoid UnicodeEncodeError
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add soeasyhub-v2 to path to import config
sys.path.append(os.path.join(os.getcwd(), 'soeasyhub-v2'))

from supabase import create_client
from matrix_config import config

def main():
    print("=" * 60)
    print("Checking Report Generation Status")
    print("=" * 60)

    if not config.is_valid():
        print("Config invalid. Check SUPABASE_URL/KEY or Token..txt")
        return

    try:
        supabase = create_client(config.supabase_url, config.supabase_key)
        
        # 1. Total count
        print("\n[1] Checking total records...")
        res_total = supabase.table("grich_keywords_pool").select("id", count="exact").execute()
        total_count = res_total.count
        print(f"   Total records: {total_count}")

        # 2. Check for existing PDFs
        print("\n[2] Checking for generated PDFs (pdf_url IS NOT NULL)...")
        res_reports = supabase.table("grich_keywords_pool") \
            .select("id, slug, pdf_url") \
            .not_.is_("pdf_url", "null") \
            .limit(10) \
            .execute()
        
        report_count = len(res_reports.data)
        print(f"   Records with PDF: {report_count}")

        if res_reports.data:
            print("\n   Sample PDF URLs (first 5):")
            for r in res_reports.data[:5]:
                print(f"   - Slug: {r['slug']}")
                print(f"     URL:  {r['pdf_url']}")
                print("-" * 40)
        else:
            print("   No PDFs found in database.")

        # 3. Check pending reports
        print("\n[3] Checking pending reports (final_article exists but pdf_url is null)...")
        res_pending = supabase.table("grich_keywords_pool") \
            .select("id, slug") \
            .not_.is_("final_article", "null") \
            .is_("pdf_url", "null") \
            .limit(10) \
            .execute()
        
        pending_count = len(res_pending.data)
        print(f"   Pending reports: {pending_count}")

        if res_pending.data:
            print("\n   Sample pending slugs (first 5):")
            for r in res_pending.data[:5]:
                print(f"   - {r['slug']}")

    except Exception as e:
        print(f"\nError querying database: {e}")

if __name__ == "__main__":
    main()
