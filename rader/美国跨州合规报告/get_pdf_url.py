import os
from supabase import create_client

def main():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: Missing SUPABASE_URL or SUPABASE_KEY environment variables.")
        return

    try:
        supabase = create_client(supabase_url, supabase_key)
        
        # Try finding the specific slug first
        target_slug = "california-electrician-reciprocity"
        # print(f"Searching for PDF URL for slug: {target_slug}...")
        
        res = supabase.table("grich_keywords_pool").select("pdf_url").eq("slug", target_slug).execute()
        
        pdf_url = None
        if res.data and len(res.data) > 0:
            pdf_url = res.data[0].get("pdf_url")
            
        if pdf_url:
            print(f"PDF URL for {target_slug}:")
            print(pdf_url)
            return

        # If not found or empty, search for ANY record with pdf_url
        # print(f"Slug {target_slug} not found or has no PDF. Searching for ANY valid PDF...")
        
        res = supabase.table("grich_keywords_pool").select("slug, pdf_url").not_.is_("pdf_url", "null").limit(1).execute()
        
        if res.data and len(res.data) > 0:
            item = res.data[0]
            print(f"Found PDF for slug: {item['slug']}")
            print(item['pdf_url'])
        else:
            print("No PDF URLs found in the database.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()