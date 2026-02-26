import os
from supabase import create_client

# Load config from Token..txt
config = {}
with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Project URL:' in line: config['url'] = line.split('URL:')[1].strip()
        if 'Secret keys:' in line: config['key'] = line.split('keys:')[1].strip()

sb = create_client(config['url'], config['key'])

# 1. 总库存数
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
total_count = total.count

# 2. 网页成品数
article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("final_article", "null").execute()
article_count = article.count

# 3. PDF 成品数
pdf = sb.table("grich_keywords_pool").select("id", count="exact")\
    .not_.is_("pdf_url", "null").execute()
pdf_count = pdf.count

# 4. 异常诊断 - 检查新词状态
blue_tags = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue").execute()
blue_count = blue_tags.count

# 检查新词的下载状态
blue_downloaded = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue")\
    .eq("is_downloaded", True).execute()
blue_downloaded_count = blue_downloaded.count

# 检查新词是否有 final_article
blue_with_article = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("color_tag", "Blue")\
    .not_.is_("final_article", "null").execute()
blue_article_count = blue_with_article.count

# 直接输出结果
print("=== 金库审计结果 ===")
print()
print(f"1. 总库存数: {total_count}")
print(f"2. 网页成品数: {article_count}")
print(f"3. PDF 成品数: {pdf_count}")
print()
print("=== 异常诊断 ===")
print(f"• 新注入真实词 (color_tag='Blue'): {blue_count} 个")
print(f"• 其中已下载的: {blue_downloaded_count} 个")
print(f"• 其中已有 final_article 的: {blue_article_count} 个")
print()
print("=== 问题分析 ===")
print("GitHub Actions 运行 11 分钟但未生产新文章的原因：")
print("1. 新注入的 102 个真实词中，只有部分已被下载")
print(f"   - 已下载: {blue_downloaded_count}/{blue_count}")
print("2. Composer 查询条件可能遗漏了新词")
print("   - 当前查询: is_downloaded=true, pdf_url=null, content_json≠null")
print(f"   - 符合条件的新词数量: 需要检查")
print("3. 可能的原因:")
print("   a) 新词尚未被 Librarian 抓取 (is_downloaded=false)")
print("   b) 新词已被抓取但 Refiner 未生成 content_json")
print("   c) 新词已有 content_json 但 Composer 查询未找到它们")
print()
print("=== 建议立即执行 ===")
print("1. 检查 Librarian 是否处理了 color_tag='Blue' 的记录")
print("2. 运行 Composer 强制模式: python soeasyhub-v2/matrix_composer.py --batch 200 --force")
print("3. 检查 GitHub Actions 日志，确认各阶段实际处理数量")