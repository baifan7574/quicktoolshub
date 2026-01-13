"""
会话记忆保存工具
将当前 Antigravity 会话的聊天记录保存到 GitHub 仓库
"""
import sys
import requests
import json
from datetime import datetime
from pathlib import Path

def save_session_to_github(session_summary, conversation_id=None):
    """
    保存会话摘要到 GitHub
    
    Args:
        session_summary: 会话摘要文本
        conversation_id: 会话 ID（可选）
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    conv_id = conversation_id or timestamp
    
    # 生成文件名
    filename = f"SESSION_{timestamp}.md"
    
    # 格式化内容
    content = f"""# Antigravity 会话记录

**会话 ID**: {conv_id}
**保存时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**保存者**: Executive (Antigravity)

---

## 会话摘要

{session_summary}

---

## 元数据
- 保存方式: 自动备份
- 目的: 跨会话记忆延续
- 下次会话: 可通过读取此文件恢复上下文

---

*此文件由会话记忆系统自动生成*
"""
    
    # n8n webhook 配置
    webhook_url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"
    payload = {
        "owner": "baifan7574",
        "repo": "grich-cloud",
        "path": f"CONVERSATION_HISTORY/{filename}",
        "content": content,
        "message": f"Save session memory: {conv_id}"
    }
    
    try:
        print(f"\n📝 正在保存会话记录到 GitHub...")
        print(f"文件路径: CONVERSATION_HISTORY/{filename}")
        print(f"会话 ID: {conv_id}")
        
        response = requests.post(webhook_url, json=payload, timeout=15)
        
        if response.status_code == 200:
            print("\n✅ 会话记录保存成功！")
            print(f"\n📂 GitHub 路径:")
            print(f"   https://github.com/baifan7574/grich-cloud/blob/main/CONVERSATION_HISTORY/{filename}")
            print(f"\n💡 新会话读取命令:")
            print(f'   python read_session_memory.py "{filename}"')
            return True
        else:
            print(f"\n❌ 保存失败: HTTP {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("    💾 Antigravity 会话记忆保存系统")
    print("="*70)
    
    if len(sys.argv) > 1:
        # 从命令行参数读取摘要
        summary = " ".join(sys.argv[1:])
    else:
        print("\n请输入本次会话的摘要（包含关键内容和完成的任务）:")
        print("-" * 70)
        print("提示：包括完成了什么、解决了什么问题、创建了哪些文件等")
        print("-" * 70)
        summary = input("➤ ")
    
    if not summary.strip():
        print("\n❌ 摘要不能为空！")
        sys.exit(1)
    
    # 尝试获取会话 ID（可选）
    conv_id_input = input("\n会话 ID (直接回车跳过): ").strip()
    conv_id = conv_id_input if conv_id_input else None
    
    # 保存到 GitHub
    success = save_session_to_github(summary, conv_id)
    
    print("\n" + "="*70)
    if success:
        print("✅ 会话记忆已保存！下次会话可以读取这些信息。")
    else:
        print("⚠️ 保存可能未成功，请检查网络和 n8n 状态")
    print("="*70 + "\n")
    
    sys.exit(0 if success else 1)
