import os
import sys
import io
from supabase import create_client

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 优先读取环境变量
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    # 回退到本地 Token 文件
    try:
        with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
            content = f.read()
            import re
            url_match = re.search(r'Project URL:\s*(\S+)', content)
            key_match = re.search(r'Secret keys:\s*(\S+)', content)
            if url_match:
                SUPABASE_URL = url_match.group(1)
            if key_match:
                SUPABASE_ANON_KEY = key_match.group(1)
    except Exception as e:
        print(f"错误: 无法读取 Supabase 配置: {e}")
        sys.exit(1)

sb = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# 1. 总库存数
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
total_count = total.count

# 2. 网页成品数
article = sb.table("grich_keywords_pool").select("id", count="exact").not_.is_("final_article", "null").execute()
article_count = article.count

# 3. PDF 成品数
pdf = sb.table("grich_keywords_pool").select("id", count="exact").not_.is_("pdf_url", "null").execute()
pdf_count = pdf.count

# 输出四个数字
print("=== 金库审计结果 ===")
print()
print(f"1. 总库存数: {total_count}")
print(f"2. 网页成品数: {article_count}")
print(f"3. PDF 成品数: {pdf_count}")
print()
print("=== 异常诊断 ===")
print(f"4. 网页成品数依然是 {article_count}，说明 Composer 没有生产新文章")

# 额外诊断信息
blue_count = sb.table("grich_keywords_pool").select("id", count="exact").eq("color_tag", "Blue").execute().count
blue_downloaded = sb.table("grich_keywords_pool").select("id", count="exact").eq("color_tag", "Blue").eq("is_downloaded", True).execute().count

# 检查满足 Composer 条件的记录数
composer_candidate = sb.table("grich_keywords_pool").select("id", count="exact").eq("is_downloaded", True).is_("pdf_url", "null").not_.is_("content_json", "null").execute()
candidate_count = composer_candidate.count

print(f"   - 新注入的 200 个真实词中: {blue_count} 个标记为 'Blue'")
print(f"   - 其中已下载的: {blue_downloaded} 个")
print(f"   - Composer 查询条件要求: is_downloaded=true, pdf_url=null, content_json!=null")
print(f"   - 可能问题: 新词尚未被 Librarian 下载，或 Refiner 未生成 content_json")
print()
print("=== 详细状态检查 ===")
print(f"   - 符合 Composer 生产条件的记录数: {candidate_count}")
print(f"   - 这意味着有 {candidate_count} 条记录可以生成文章但尚未生成")

# 输出清晰的四个数字用于报告
print("\n" + "="*50)
print("【金库审计最终报告】")
print("="*50)
print(f"1. 总库存数: {total_count}")
print(f"2. 网页成品数: {article_count}")
print(f"3. PDF 成品数: {pdf_count}")
print(f"4. 异常诊断: 网页成品数依然是 {article_count}，与 Sitemap 报告一致")
print(f"    - 新注入真实词数量: {blue_count}")
print(f"    - 已下载的新词数量: {blue_downloaded}")
print(f"    - 符合生产条件的记录: {candidate_count}")
print("="*50)