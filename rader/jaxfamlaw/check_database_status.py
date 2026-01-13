import requests
import json
from datetime import datetime

# 读取环境变量
env_path = r'd:\quicktoolshub\雷达监控。\GRICH\grich-astro\.env'
env_vars = {}

try:
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
except Exception as e:
    print(f"❌ Error reading .env file: {e}")
    exit(1)

SUPABASE_URL = env_vars.get("PUBLIC_SUPABASE_URL")
SUPABASE_KEY = env_vars.get("PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print(f"❌ Error: Supabase credentials not found")
    exit(1)

# Supabase REST API
REST_URL = f"{SUPABASE_URL}/rest/v1/lawsuits"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

print("="*60)
print("🔍 GRICH 数据库状态检查")
print("="*60)
print(f"📡 连接到: {SUPABASE_URL[:40]}...")
print()

try:
    # 1. 获取总记录数
    response = requests.get(REST_URL, headers=HEADERS, timeout=10)
    
    if response.status_code != 200:
        print(f"❌ API请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        exit(1)
    
    data = response.json()
    total_count = len(data)
    
    print(f"📊 数据库总记录数: {total_count}")
    print()
    
    if total_count == 0:
        print("⚠️ 数据库为空！")
        print("❌ 结论: 两个引擎都没有成功运行过")
        print()
        print("建议操作:")
        print("  1. 运行全网捕鱼引擎: python scripts/seed_engine_serper.py")
        print("  2. 或运行狙击引擎: python scripts/seed_engine_courtlistener.py")
    else:
        print(f"✅ 数据库有数据！共 {total_count} 条记录")
        print()
        
        # 2. 分析数据来源
        print("📋 数据详情:")
        print("-" * 60)
        
        # 统计品牌
        brands = {}
        for record in data:
            brand = record.get('brand_name', 'Unknown')
            brands[brand] = brands.get(brand, 0) + 1
        
        print(f"   品牌数量: {len(brands)}")
        print(f"   Top 10 品牌:")
        sorted_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]
        for brand, count in sorted_brands:
            print(f"     - {brand}: {count} 条案件")
        
        print()
        
        # 3. 显示最新的5条记录
        print("📝 最新5条记录:")
        print("-" * 60)
        for i, record in enumerate(data[:5], 1):
            print(f"{i}. 品牌: {record.get('brand_name', 'N/A')}")
            print(f"   案号: {record.get('case_number', 'N/A')}")
            print(f"   法院: {record.get('court', 'N/A')}")
            print(f"   风险分: {record.get('risk_score', 'N/A')}")
            print(f"   数据源: {record.get('raw_data_url', 'N/A')[:50]}...")
            print()
        
        # 4. 判断数据来源
        print("🔍 数据来源分析:")
        print("-" * 60)
        
        justia_count = sum(1 for r in data if 'justia' in str(r.get('raw_data_url', '')).lower())
        courtlistener_count = sum(1 for r in data if 'courtlistener' in str(r.get('raw_data_url', '')).lower())
        
        print(f"   Justia来源 (全网捕鱼): {justia_count} 条")
        print(f"   CourtListener来源 (狙击): {courtlistener_count} 条")
        print(f"   其他来源: {total_count - justia_count - courtlistener_count} 条")
        print()
        
        if justia_count > 0:
            print("✅ 全网捕鱼引擎 (seed_engine_serper.py) 已执行")
        if courtlistener_count > 0:
            print("✅ 狙击引擎 (seed_engine_courtlistener.py) 已执行")
        
        if justia_count == 0 and courtlistener_count == 0:
            print("⚠️ 无法确定数据来源（可能是测试数据）")

except Exception as e:
    print(f"❌ 检查失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
print("检查完成")
print("="*60)
