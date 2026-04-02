import os
from supabase import create_client

# Load config from Token..txt
config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# 1. Total inventory
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
total_count = total.count

# 2. Web articles produced
article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("final_article", "null").execute()
article_count = article.count

# 3. PDFs produced
pdf = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("pdf_url", "null").execute()
pdf_count = pdf.count

# 4. New real keywords (color_tag='Blue')
blue_tags = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue").execute()
blue_count = blue_tags.count

# 5. New keywords downloaded
blue_downloaded = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue")\
    .eq("is_downloaded", True).execute()
blue_downloaded_count = blue_downloaded.count

# 6. New keywords with final_article
blue_with_article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue")\
    .not_.is_("final_article", "null").execute()
blue_article_count = blue_with_article.count

# 7. Check Composer query conditions
composer_ready = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null").execute()
composer_ready_count = composer_ready.count

# 8. Check if new keywords are in Composer queue
blue_in_composer = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null").execute()
blue_in_composer_count = blue_in_composer.count

print("AUDIT RESULTS")
print("-------------")
print(f"1. Total inventory (rows in grich_keywords_pool): {total_count}")
print(f"2. Web articles produced (final_article not null): {article_count}")
print(f"3. PDFs produced (pdf_url not null): {pdf_count}")
print()
print("DIAGNOSIS")
print("---------")
print(f"• New real keywords (color_tag='Blue'): {blue_count}")
print(f"• New keywords downloaded (is_downloaded=true): {blue_downloaded_count}")
print(f"• New keywords with final_article: {blue_article_count}")
print(f"• Records ready for Composer (downloaded, no PDF, has content): {composer_ready_count}")
print(f"• New keywords ready for Composer: {blue_in_composer_count}")
print()
print("ANALYSIS")
print("--------")
print("GitHub Actions ran 11 minutes but produced no new articles because:")
print(f"1. Only {blue_downloaded_count} of {blue_count} new keywords are downloaded.")
print(f"2. Composer queue has {composer_ready_count} records, but only {blue_in_composer_count} are new keywords.")
print("3. The query condition in matrix_composer.py may be too restrictive.")
print("   It requires: is_downloaded=true, pdf_url=null, content_json!=null")
print("   But new keywords may not have content_json yet (needs Refiner).")
print()
print("IMMEDIATE ACTION")
print("----------------")
print("1. Check why Librarian didn't download all new keywords.")
print("2. Run Refiner to generate content_json for downloaded new keywords.")
print("3. Run Composer in force mode: python soeasyhub-v2/matrix_composer.py --batch 200 --force")