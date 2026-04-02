import os
import requests
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def load_config():
    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
    return config

def audit():
    config = load_config()
    supabase = create_client(config['url'], config['key'])
    
    print("🕵️  PDF 真实性大审计启动...")
    
    # 1. 统计数据库中标记为已下载的数量
    res = supabase.table("grich_keywords_pool").select("id, slug").eq("is_downloaded", True).execute()
    db_count = len(res.data)
    
    # 2. 扫描 Storage 桶中的真实文件
    try:
        files = supabase.storage.from_("raw-handbooks").list()
        storage_count = len(files)
    except:
        storage_count = 0

    print(f"📊 基础指标：")
    print(f"   - 数据库标记下载：{db_count} 篇")
    print(f"   - 库房实存文件：{storage_count} 篇")
    
    # 3. 随机抽检 (验证文件是否真的是 PDF)
    if files:
        sample = files[0]
        name = sample['name']
        print(f"🧐 正在抽检样板文件: {name}")
        
        # 下载一小段文件头验证
        try:
            file_data = supabase.storage.from_("raw-handbooks").download(name)
            if file_data[:4] == b'%PDF':
                print("✅ 验证通过：文件头符合标准 PDF 协议，是真货。")
            else:
                print("❌ 验证失败：文件内容可能是一个 404 网页伪装的。")
        except Exception as e:
            print(f"⚠️ 无法下载文件进行审计: {e}")

    print("\n💡 厂长，验证逻辑已就绪。目前抓取的 PDF 只要能通过‘文件头校验’，就说明它不是报错网页，而是实打实的文件。")

if __name__ == "__main__":
    audit()
