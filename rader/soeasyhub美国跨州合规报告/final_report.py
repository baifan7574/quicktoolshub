import os
import json
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

def main():
    print("Generating Final Battle Report...")
    
    try:
        supabase_url, supabase_key = load_credentials()
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Total count
        res = supabase.table("grich_keywords_pool").select("id", count="exact", head=True).execute()
        total_count = res.count
        
        # Downloaded count
        res_dl = supabase.table("grich_keywords_pool").select("id", count="exact", head=True).eq("is_downloaded", True).execute()
        downloaded_count = res_dl.count
        
        # Refined count
        res_ref = supabase.table("grich_keywords_pool").select("id", count="exact", head=True).eq("is_refined", True).execute()
        refined_count = res_ref.count
        
        # Final Article count (not null)
        res_art = supabase.table("grich_keywords_pool").select("id", count="exact", head=True).not_.is_("final_article", "null").execute()
        article_count = res_art.count
        
        print(f"Total Keywords: {total_count}")
        print(f"Downloaded (Ready for Refiner): {downloaded_count}")
        print(f"Refined (Ready for Composer): {refined_count}")
        print(f"Articles Produced: {article_count}")
        
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    main()
