import requests
import json
import os
import time
from datetime import datetime

# 修复环境路径 - 使用项目根目录.env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
env_vars = {}

try:
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
except Exception as e:
    print(f"环境文件读取错误: {e}")
    exit(1)

# 环境变量配置
SUPABASE_URL = env_vars.get("PUBLIC_SUPABASE_URL")
SUPABASE_KEY = env_vars.get("SUPABASE_SERVICE_KEY")
SERPER_API_KEY = env_vars.get("SERPER_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, SERPER_API_KEY]):
    print("缺少必需环境变量")
    exit(1)

# 数据库配置
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# 品牌数据文件路径
BRANDS_FILE = os.path.join(os.path.dirname(__file__), '..', 'sql', 'brands_1000.json')

print("="*70)
print("启动律所案件搜索引擎")
print("="*70)

# 其余代码保持不变...
