import os
from supabase import create_client

# Load config from Token..txt
config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

print("=== 金库审计报告 ===")
print()

# 1. 总库存数
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
print(f"1. 总库存数 (grich_keywords_pool 表总行数): {total.count}")

# 2. 网页成品数
article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("final_article", "null").execute()
print(f"2. 网页成品数 (final_article 不为空): {article.count}")

# 3. PDF 成品数
pdf = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("pdf_url", "null").execute()
print(f"3. PDF 成品数 (pdf_url 不为空): {pdf.count}")

# 4. 异常诊断 - 详细分析
print()
print("=== 异常诊断 ===")

# 4.1 检查未下载记录
not_downloaded = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", False).execute()
print(f"4.1 未下载记录 (is_downloaded=false): {not_downloaded.count}")

# 4.2 检查已下载但无 content_json 的记录
downloaded_no_content = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("content_json", "null").execute()
print(f"4.2 已下载但无内容 (content_json=null): {downloaded_no_content.count}")

# 4.3 检查有 content_json 但无 final_article 的记录
content_no_article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("content_json", "null")\
    .is_("final_article", "null").execute()
print(f"4.3 有内容但无文章 (final_article=null): {content_no_article.count}")

# 4.4 检查有 final_article 但无 pdf_url 的记录
article_no_pdf = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("final_article", "null")\
    .is_("pdf_url", "null").execute()
print(f"4.4 有文章但无PDF (pdf_url=null): {article_no_pdf.count}")

# 4.5 检查新注入的真实词 (color_tag='Blue')
blue_tags = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue").execute()
print(f"4.5 新注入真实词 (color_tag='Blue'): {blue_tags.count}")

# 4.6 检查最近创建的记录 (假设有 created_at 字段)
# 先检查 created_at 字段是否存在，使用一个简单查询
try:
    recent = sb.table("grich_keywords_pool").select("id", count="exact")\
        .order("created_at", desc=True).limit(10).execute()
    # 没有错误说明字段存在
    print(f"4.6 最近记录检查: created_at 字段存在")
except Exception as e:
    print(f"4.6 最近记录检查: created_at 字段可能不存在 - {e}")

# 4.7 检查 Librarian 查询逻辑
print()
print("=== 生产流水线阻塞点 ===")
print(f"• Librarian 原料: {not_downloaded.count} 个未下载记录")
print(f"• Refiner 原料: {downloaded_no_content.count} 个已下载但无内容记录")
print(f"• Composer 原料: {content_no_article.count} 个有内容但无文章记录")
print(f"• Reporter 原料: {article_no_pdf.count} 个有文章但无PDF记录")

# 4.8 如果网页成品数依然是 131，分析原因
if article.count == 131:
    print()
    print("❌ 问题诊断：网页成品数依然为 131，说明 Composer 没有生产新文章")
    print("可能原因：")
    print("1. Composer 查询条件太严格：需要检查 matrix_composer.py 的 fetch_records 方法")
    print("2. 新词没有被 Librarian 抓取：需要检查 matrix_librarian.py 的 fetch_pending_tasks 方法")
    print("3. 新词虽然被标记为 color_tag='Blue'，但查询条件未包含此标签")
    print("4. GitHub Actions 可能因为错误而跳过了某些阶段")
    print()
    print("建议立即检查：")
    print("• 运行 python soeasyhub-v2/matrix_librarian.py 查看是否处理新词")
    print("• 运行 python soeasyhub-v2/matrix_composer.py --batch 200 强制处理")

print()
print("=== 审计完成 ===")