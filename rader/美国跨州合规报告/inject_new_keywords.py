import os
import csv
import sys
import codecs
from supabase import create_client, Client

# 设置标准输出编码为 utf-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 1. 环境校验与客户端创建
TOKEN_FILE = os.path.join(".agent", "Token..txt")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    # 尝试读取本地 Token 文件作为后备
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'Project URL:' in line:
                    supabase_url = line.split('Project URL:')[1].strip()
                if 'Secret keys:' in line:
                    # 注意：这里读取的是 anon key 还是 service_role key 取决于 Token 文件内容
                    # 通常写操作需要 service_role key，或者启用 RLS 的 anon key
                    # 假设这里是 service_role key
                    supabase_key = line.split('Secret keys:')[1].strip()
    except Exception as e:
        print(f"⚠️ 无法读取本地 Token 文件: {e}")

if not supabase_url or not supabase_key:
    print("❌ 错误：未找到 Supabase URL 或 Key。")
    sys.exit(1)

try:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✅ 成功创建 Supabase 客户端")
except Exception as e:
    print(f"❌ 创建客户端失败: {e}")
    sys.exit(1)

# 2. 读取 CSV 词库
CSV_FILE = "heavy_mine_20260113.csv"
target_keywords = []

if not os.path.exists(CSV_FILE):
    print(f"❌ 错误：未找到词库文件 {CSV_FILE}")
    sys.exit(1)

print(f"📂 正在读取词库: {CSV_FILE} ...")
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row.get('slug') or row.get('keyword') or row.get('Keyword') or list(row.values())[0]
            if kw:
                target_keywords.append(kw.strip().lower())
except Exception as e:
    print(f"❌ 读取 CSV 失败: {e}")
    sys.exit(1)

print(f"📊 词库中共读取到 {len(target_keywords)} 个候选词")

# 3. 获取现有词库 (黑名单)
# 由于 supabase-py 的 select limit 默认是 1000，如果数据量大需要分页
# 这里假设目前只有 131 条，或者我们分批查询
existing_slugs = set()
try:
    # 分页获取所有 slug
    has_more = True
    page = 0
    page_size = 1000
    while has_more:
        res = supabase.table("grich_keywords_pool").select("slug").range(page * page_size, (page + 1) * page_size - 1).execute()
        data = res.data
        if not data:
            has_more = False
        else:
            for row in data:
                existing_slugs.add(row['slug'])
            if len(data) < page_size:
                has_more = False
            page += 1
            
    print(f"🛡️ 数据库中已存在 {len(existing_slugs)} 个词 (将被跳过)")
except Exception as e:
    print(f"❌ 查询现有词失败: {e}")
    # 允许继续，可能只是第一次运行表为空
    pass

# 4. 筛选 200 个新词
new_keywords_to_insert = []
count = 0
TARGET_COUNT = 200

def make_slug(text):
    return text.lower().replace(" ", "-").replace("/", "-").replace("--", "-")

for kw in target_keywords:
    slug = make_slug(kw)
    if slug not in existing_slugs and slug not in new_keywords_to_insert:
        new_keywords_to_insert.append(slug)
        count += 1
        if count >= TARGET_COUNT:
            break

if len(new_keywords_to_insert) < TARGET_COUNT:
    print(f"⚠️ 警告: 词库中仅找到 {len(new_keywords_to_insert)} 个新词，未达到 200 个的目标。")
    
    # 补救措施：生成更多长尾词
    states = ["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina", "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west-virginia", "wisconsin", "wyoming"]
    professions = ["nurse", "electrician", "teacher", "cpa", "engineer", "plumber", "real estate agent", "dental hygienist", "pharmacist", "psychologist"]
    
    print("🔄 启动自动补全逻辑...")
    for state in states:
        if len(new_keywords_to_insert) >= TARGET_COUNT: break
        for prof in professions:
            if len(new_keywords_to_insert) >= TARGET_COUNT: break
            
            slug1 = make_slug(f"{state} {prof} license reciprocity")
            if slug1 not in existing_slugs and slug1 not in new_keywords_to_insert:
                new_keywords_to_insert.append(slug1)
                
            if len(new_keywords_to_insert) >= TARGET_COUNT: break
            slug2 = make_slug(f"{prof} license reciprocity {state}")
            if slug2 not in existing_slugs and slug2 not in new_keywords_to_insert:
                new_keywords_to_insert.append(slug2)

print(f"🎯 最终准备插入 {len(new_keywords_to_insert)} 个新词")

# 5. 执行插入
inserted_count = 0
if new_keywords_to_insert:
    try:
        # Supabase 批量插入
        data_to_insert = [
            {
                "slug": slug,
                "is_downloaded": False,
                "is_refined": False,
                # "created_at": "NOW()", # Supabase 会自动处理默认值，或者在这里传递 ISO 字符串
                "color_tag": "Green"
            }
            for slug in new_keywords_to_insert
        ]
        
        # 分批插入，防止请求过大
        batch_size = 50
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i + batch_size]
            res = supabase.table("grich_keywords_pool").insert(batch).execute()
            inserted_count += len(res.data)
            
        print(f"✅ 成功插入 {inserted_count} 行新数据")
        
    except Exception as e:
        print(f"❌ 插入失败: {e}")
        # 不退出，继续验证
else:
    print("⚠️ 没有新词需要插入")

# 6. 最终验证
try:
    res = supabase.table("grich_keywords_pool").select("slug", count="exact", head=True).execute()
    final_count = res.count
    print(f"🏁 数据库当前总行数: {final_count}")
    print(f"🚀 增量计划执行完毕。新增: {inserted_count}。")
except Exception as e:
    print(f"❌ 验证失败: {e}")
