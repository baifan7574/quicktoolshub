import os
import sys
sys.path.append('soeasyhub-v2')

from supabase import create_client

# Load config from Token..txt
config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

print("=== Simple & Brutal 生产逻辑测试 ===")

# 1. Composer 查询条件：已下载、无 PDF、有 content_json
composer_query = sb.table("grich_keywords_pool").select("id, slug, keyword, is_downloaded, pdf_url")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null")\
    .order("id", desc=False)\
    .limit(10)\
    .execute()

print(f"\n1. Composer 待处理记录 (is_downloaded=true, pdf_url=null, content_json≠null)：")
print(f"   总数（全库）: {len(composer_query.data)} 条（仅显示前10条）")
for i, r in enumerate(composer_query.data[:5]):
    print(f"   {i+1}. ID:{r['id']} - {r['slug']}")

# 2. Reporter 查询条件：已下载、无 PDF、有 final_article
reporter_query = sb.table("grich_keywords_pool").select("id, slug, keyword, is_downloaded, pdf_url, final_article")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("final_article", "null")\
    .order("id", desc=False)\
    .limit(10)\
    .execute()

print(f"\n2. Reporter 待处理记录 (is_downloaded=true, pdf_url=null, final_article≠null)：")
print(f"   总数（全库）: {len(reporter_query.data)} 条（仅显示前10条）")
for i, r in enumerate(reporter_query.data[:5]):
    print(f"   {i+1}. ID:{r['id']} - {r['slug']}")

# 3. 统计各状态数量
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
total_count = total.count
print(f"\n3. 数据库总记录数: {total_count}")

downloaded = sb.table("grich_keywords_pool").select("id", count="exact").eq("is_downloaded", True).execute()
print(f"   已下载 (is_downloaded=true): {downloaded.count}")

has_content = sb.table("grich_keywords_pool").select("id", count="exact").not_.is_("content_json", "null").execute()
print(f"   有内容数据 (content_json≠null): {has_content.count}")

has_article = sb.table("grich_keywords_pool").select("id", count="exact").not_.is_("final_article", "null").execute()
print(f"   已生成文章 (final_article≠null): {has_article.count}")

has_pdf = sb.table("grich_keywords_pool").select("id", count="exact").not_.is_("pdf_url", "null").execute()
print(f"   已生成 PDF (pdf_url≠null): {has_pdf.count}")

# 4. 计算待处理流水线
pipeline_ready = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null")\
    .execute()
print(f"\n4. 生产流水线待处理总数 (Composer): {pipeline_ready.count}")

pipeline_reporter = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("final_article", "null")\
    .execute()
print(f"   PDF 生成待处理总数 (Reporter): {pipeline_reporter.count}")

print("\n=== 测试完成 ===")