import os
import sys
import codecs
from supabase import create_client, Client

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

TOKEN_FILE = os.path.join(".agent", "Token..txt")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.split('\n'):
                    if 'Project URL:' in line:
                        supabase_url = line.split('Project URL:')[1].strip()
                    if 'Secret keys:' in line:
                        supabase_key = line.split('Secret keys:')[1].strip()
    except Exception as e: pass

supabase: Client = create_client(supabase_url, supabase_key)

try:
    res = supabase.table("grich_keywords_pool").select("slug").limit(20).execute()
    print("数据库中现有 Slug 样本:")
    for row in res.data:
        print(f"- {row['slug']}")
except Exception as e:
    print(f"查询失败: {e}")
