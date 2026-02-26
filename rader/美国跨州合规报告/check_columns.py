import os
from supabase import create_client, Client

def load_credentials():
    """加载 Supabase 凭据，优先使用环境变量"""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        return supabase_url, supabase_key
    
    # 后备：从 Token..txt 读取
    token_paths = [
        ".agent/Token..txt",
        os.path.join(".agent", "Token..txt"),
        r"d:\quicktoolshub\rader\美国跨州合规报告\.agent\Token..txt"
    ]
    
    for token_path in token_paths:
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    url = None
                    key = None
                    for line in content.split('\n'):
                        if 'Project URL:' in line:
                            url = line.split('Project URL:')[1].strip()
                        if 'Secret keys:' in line:
                            key = line.split('Secret keys:')[1].strip()
                    if url and key:
                        print(f"[INFO] 从 {token_path} 读取凭据")
                        return url, key
            except Exception as e:
                print(f"[ERROR] 读取 {token_path} 失败: {e}")
    
    raise ValueError(
        "未找到 Supabase 凭据。请设置环境变量 SUPABASE_URL 和 SUPABASE_KEY，或创建 .agent/Token..txt 文件。"
        "禁止在代码中硬编码密钥！"
    )

def check_columns():
    try:
        url, key = load_credentials()
        supabase: Client = create_client(url, key)
        res = supabase.table("grich_keywords_pool").select("*").limit(1).execute()
        if res.data:
            print(f"Available columns: {res.data[0].keys()}")
        else:
            print("No data in table to infer columns.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
