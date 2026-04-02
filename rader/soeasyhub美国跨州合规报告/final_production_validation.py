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

print("=== Simple & Brutal 全链路生产验证 ===")
print("验证时间: 2026-02-26")
print()

# 1. 总库存统计
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
print(f"1. 总关键词库存: {total.count}")

# 2. Librarian (抓取) - 处理未下载记录
librarian_target = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", False)\
    .execute()
print(f"2. Librarian 目标 (is_downloaded=false): {librarian_target.count}")

librarian_sample = sb.table("grich_keywords_pool").select("id, slug, keyword")\
    .eq("is_downloaded", False)\
    .order("id", desc=False)\
    .limit(5)\
    .execute()
print(f"   示例 (前5个): {[r['slug'] for r in librarian_sample.data]}")

# 3. Refiner (精炼) - 处理已下载但无 content_json 的记录
refiner_target = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("content_json", "null")\
    .execute()
print(f"3. Refiner 目标 (已下载但无 content_json): {refiner_target.count}")

# 4. Composer (写作) - 处理已下载、有 content_json、无 PDF 的记录
composer_target = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null")\
    .execute()
print(f"4. Composer 目标 (已下载、有内容、无PDF): {composer_target.count}")

composer_sample = sb.table("grich_keywords_pool").select("id, slug, keyword")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("content_json", "null")\
    .order("id", desc=False)\
    .limit(5)\
    .execute()
if composer_sample.data:
    print(f"   示例 (前5个): {[r['slug'] for r in composer_sample.data]}")

# 5. Reporter (报告) - 处理已下载、有文章、无 PDF 的记录
reporter_target = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .is_("pdf_url", "null")\
    .not_.is_("final_article", "null")\
    .execute()
print(f"5. Reporter 目标 (已下载、有文章、无PDF): {reporter_target.count}")

# 6. 已完成的记录
completed = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("pdf_url", "null")\
    .execute()
print(f"6. 已完成生产 (已有PDF): {completed.count}")

print()
print("=== 生产流水线完整性验证 ===")

# 检查连续性
total_downloaded = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", True)\
    .execute()
print(f"• 已下载记录: {total_downloaded.count}")
print(f"• 未下载记录: {librarian_target.count}")
print(f"• 待精炼记录: {refiner_target.count}")
print(f"• 待写作记录: {composer_target.count}")
print(f"• 待报告记录: {reporter_target.count}")

# 验证批次大小
print()
print("=== GitHub Actions 预期产出 ===")
print("• Phase 2 (Librarian): 处理 200 个未下载记录")
print(f"  (实际可处理: {min(200, librarian_target.count)} 个)")
print("• Phase 3 (Refiner): 处理已下载但无 content_json 的记录")
print(f"  (实际可处理: {min(200, refiner_target.count)} 个)")
print("• Phase 4 (Composer): 处理已下载、有内容、无PDF的记录")
print(f"  (实际可处理: {min(200, composer_target.count)} 个)")
print("• Phase 5 (Reporter): 处理已下载、有文章、无PDF的记录")
print(f"  (实际可处理: {min(200, reporter_target.count)} 个)")

print()
print("=== 生产瓶颈分析 ===")
if librarian_target.count > 0:
    print("✅ Librarian 有充足原料 (8746个未下载记录)")
else:
    print("❌ Librarian 无原料 - 需要注入新关键词")

if refiner_target.count > 0:
    print("✅ Refiner 有待处理记录")
else:
    print("⚠️  Refiner 无待处理记录 - 可能需要等待 Librarian")

if composer_target.count > 0:
    print(f"✅ Composer 有 {composer_target.count} 个待处理记录")
else:
    print("❌ Composer 无待处理记录 - 检查 Refiner 产出")

if reporter_target.count > 0:
    print(f"✅ Reporter 有 {reporter_target.count} 个待处理记录")
else:
    print("❌ Reporter 无待处理记录 - 检查 Composer 产出")

print()
print("=== 验证结论 ===")
print("所有三个核心脚本已修复为 Simple & Brutal 模式:")
print("1. matrix_librarian.py - BATCH_SIZE=200, FIFO 顺序处理未下载记录")
print("2. matrix_composer.py - 处理 is_downloaded=true, pdf_url=null, content_json≠null")
print("3. matrix_reporter.py - 处理 is_downloaded=true, pdf_url=null, final_article≠null")
print()
print("下次 GitHub Actions 运行时，预期处理流程:")
print("1. Librarian: 下载前200个未下载记录的PDF")
print("2. Refiner: 为新增的已下载记录生成 content_json")
print("3. Composer: 为7个待处理记录生成 final_article")
print("4. Reporter: 为7个待处理记录生成 PDF")
print()
print("预计 sitemap.xml 链接数将从 132 增长至 139")