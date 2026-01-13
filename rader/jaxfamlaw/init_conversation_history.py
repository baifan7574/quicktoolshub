"""
初始化 CONVERSATION_HISTORY 文件夹
"""
import requests
import json

webhook_url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"

# 创建 README 文件来初始化文件夹
payload = {
    "owner": "baifan7574",
    "repo": "grich-cloud",
    "path": "CONVERSATION_HISTORY/README.md",
    "content": """# Antigravity 会话记忆库

此文件夹用于存储 Antigravity AI 的跨会话记忆。

## 用途
- 保存老窗口的会话摘要
- 让新窗口 AI 能够读取历史上下文
- 实现跨会话的记忆延续

## 文件命名规则
- `SESSION_YYYY-MM-DD_HH-MM-SS.md` - 会话记录文件

## 使用方法

### 保存会话
```bash
python save_session_memory.py
```

### 读取会话
```bash
python read_session_memory.py
```

---

*此文件夹由 AI 记忆系统自动管理*
""",
    "message": "Initialize CONVERSATION_HISTORY folder"
}

print("正在创建 CONVERSATION_HISTORY 文件夹...")
response = requests.post(webhook_url, json=payload, timeout=15)

if response.status_code == 200:
    print("✅ 文件夹创建成功!")
    print("GitHub 路径: https://github.com/baifan7574/grich-cloud/tree/main/CONVERSATION_HISTORY")
else:
    print(f"❌ 创建失败: {response.status_code}")
    print(response.text)
