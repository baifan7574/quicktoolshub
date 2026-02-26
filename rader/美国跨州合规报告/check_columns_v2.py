import os
from supabase import create_client
import sys

# 设置编码以避免控制台编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def check_columns():
    # 优先使用环境变量
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        # 后备方案：从 Token..txt 读取
        token_path = os.path.join(".agent", "Token..txt")
        if os.path.exists(token_path):
            with open(token_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.split('\n'):
                    if 'Project URL:' in line:
                        url = line.split('Project URL:')[1].strip()
                    if 'Secret keys:' in line:
                        key = line.split('Secret keys:')[1].strip()
        
    if not url or not key:
        print("无法获取 Supabase 凭据")
        return

    try:
        sb = create_client(url, key)
        # 获取一行数据来推断列名
        res = sb.table('grich_keywords_pool').select('*').limit(1).execute()
        if res.data and len(res.data) > 0:
            print("Columns found:", res.data[0].keys())
        else:
            print("Table empty or no access")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()