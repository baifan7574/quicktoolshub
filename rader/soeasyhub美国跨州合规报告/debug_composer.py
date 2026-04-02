import os
import sys
import socket
import requests
from supabase import create_client, Client

# ================= Configuration =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")

def check_dns(hostname):
    try:
        addr = socket.gethostbyname(hostname)
        return f"✅ DNS OK: {hostname} -> {addr}"
    except Exception as e:
        return f"❌ DNS ERROR: {hostname} -> {e}"

def load_config():
    config = {}
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if "Project URL:" in line:
                config['url'] = line.split("URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("keys:")[1].strip()
            if "DSAPI:" in line:
                config['ds_key'] = line.split("DSAPI:")[1].strip()
            if "groqapi" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    config['groq_key'] = parts[1].strip()
    return config

def main():
    print("======== 🔍 SYSTEM DIAGNOSTICS START ========")
    
    # 1. Python & Environment
    print(f"🐍 Python Version: {sys.version}")
    print(f"📂 Current Dir: {os.getcwd()}")
    
    # 2. DNS & Connectivity Tests
    print("\n🌐 Testing Network Connectivity...")
    print(check_dns("google.com"))
    print(check_dns("nbfzhxgkfljeuoncujum.supabase.co"))
    print(check_dns("api.groq.com"))
    print(check_dns("api.deepseek.com"))
    
    # 3. Config Loading
    print("\n📜 Loading Token Config...")
    config = load_config()
    if not config:
        print("❌ ERROR: Token..txt not found or empty.")
        return
    
    print(f"✅ Supabase URL found: {config.get('url')}")
    print(f"✅ DeepSeek Key: {'Found' if config.get('ds_key') else 'NOT FOUND'}")
    print(f"✅ Groq Key: {'Found' if config.get('groq_key') else 'NOT FOUND'}")
    
    # 4. Supabase Connection Test
    print("\n🔌 Testing Supabase Connection...")
    try:
        supabase: Client = create_client(config['url'], config['key'])
        # Try a simple select to test table and connection
        print("📊 Querying database task counts...")
        
        # Check total records
        res_total = supabase.table("grich_keywords_pool").select("id", count="exact").limit(1).execute()
        print(f"   📈 Total keywords in pool: {res_total.count}")
        
        # Check refined but unwritten
        res_ready = supabase.table("grich_keywords_pool")\
            .select("id", count="exact")\
            .neq("content_json", "null")\
            .is_("final_article", "null")\
            .execute()
        print(f"   🎯 Records ready for Composer: {res_ready.count}")
        
        # Check downloaded but unrefined
        res_downloaded = supabase.table("grich_keywords_pool")\
            .select("id", count="exact")\
            .eq("is_downloaded", True)\
            .is_("content_json", "null")\
            .execute()
        print(f"   📦 Records ready for Refiner: {res_downloaded.count}")

    except Exception as e:
        print(f"❌ SUPABASE CONNECTION FAILED: {e}")

    print("\n======== 🔍 DIAGNOSTICS COMPLETE ========")

if __name__ == "__main__":
    main()
