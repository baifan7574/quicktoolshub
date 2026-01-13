import requests
import json
from datetime import datetime

# 测试消息
test_message = f"""
🎯 测试消息来自执行官 (Executive)

发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
测试目的: 验证 G 盘自动同步到云端
状态: 这是一条测试消息，如果您在 Google Drive 云端看到这条消息，说明双线合拢完全正常！

---
Executive → n8n → G盘 → Google Drive 云端
"""

url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"
payload = {
    "owner": "baifan7574",
    "repo": "grich-cloud",
    "path": "TEST_MESSAGE.md",
    "content": test_message,
    "message": "Test message from Executive to CTO"
}

try:
    print("正在发送测试消息到 n8n webhook...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅ Webhook 响应成功！")
        print(f"响应内容: {response.text}")
        print("\n请执行以下命令查看 G 盘本地文件内容：")
        print('Get-Content "G:\\我的云端硬盘\\GRICH_AI_BRAIN\\GRICH_MASTER_LOG.md" -Tail 20 -Encoding UTF8')
        print("\n然后在 Google Drive 网页端搜索 'GRICH_MASTER_LOG.md' 查看是否已同步！")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"响应: {response.text}")
        
except Exception as e:
    print(f"❌ 发生错误: {e}")
