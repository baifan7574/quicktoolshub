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

print("=== Simple & Brutal Librarian 逻辑测试 ===")

# 1. 统计未下载记录
total_not_downloaded = sb.table("grich_keywords_pool").select("id", count="exact")\
    .eq("is_downloaded", False)\
    .execute()
print(f"\n1. 未下载记录总数 (is_downloaded=false): {total_not_downloaded.count}")

# 2. 模拟 Librarian 查询（按 ID 升序，取前 200）
librarian_query = sb.table("grich_keywords_pool").select("id, slug, keyword, is_downloaded")\
    .eq("is_downloaded", False)\
    .order("id", desc=False)\
    .limit(200)\
    .execute()

print(f"2. Librarian 将处理的记录 (前200个):")
print(f"   实际获取数量: {len(librarian_query.data)}")
for i, r in enumerate(librarian_query.data[:10]):
    print(f"   {i+1}. ID:{r['id']} - {r['slug']}")

# 3. 验证排序是否正确
ids = [r['id'] for r in librarian_query.data]
sorted_ids = sorted(ids)
if ids == sorted_ids:
    print("   ✅ 排序正确: ID 升序 (FIFO)")
else:
    print("   ❌ 排序错误: ID 未按升序排列")

# 4. 验证这些记录是否确实未下载
all_not_downloaded = all(r['is_downloaded'] == False for r in librarian_query.data)
if all_not_downloaded:
    print("   ✅ 所有记录均为未下载状态")
else:
    print("   ❌ 存在已下载记录混入")

# 5. 检查工作流完整性
print(f"\n3. 生产流水线完整性检查:")
print(f"   - 未下载记录: {total_not_downloaded.count}")
print(f"   - 已下载但未处理: {len(librarian_query.data)} 个即将被 Librarian 抓取")

# 6. 模拟 Librarian 处理后的下游影响
print(f"\n4. 下游影响预测:")
print(f"   - Librarian 处理这 {len(librarian_query.data)} 个记录后，")
print(f"     它们将变为 is_downloaded=true")
print(f"   - 然后 Matrix Refiner 将为它们生成 content_json")
print(f"   - 接着 Matrix Composer 将使用 content_json 生成 final_article")
print(f"   - 最后 Matrix Reporter 将生成 PDF")

# 7. 统计整体生产漏斗
total = sb.table("grich_keywords_pool").select("id", count="exact").execute()
print(f"\n5. 整体生产漏斗 (总数 {total.count}):")
print(f"   - 未下载: {total_not_downloaded.count} ({total_not_downloaded.count/total.count*100:.1f}%)")
print(f"   - 已下载但无 content_json: 待 Refiner 处理")
print(f"   - 有 content_json 但无 final_article: 待 Composer 处理")
print(f"   - 有 final_article 但无 pdf_url: 待 Reporter 处理")

print("\n=== 测试完成 ===")