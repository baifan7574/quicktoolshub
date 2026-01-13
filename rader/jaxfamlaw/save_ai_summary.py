"""
AI 智能会话保存工具
自动生成摘要并保存到 GitHub
"""
import sys
import requests
from datetime import datetime

def save_ai_summary_to_github(ai_summary):
    """
    保存 AI 生成的摘要到 GitHub
    
    Args:
        ai_summary: AI 自动生成的会话摘要
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"SESSION_{timestamp}.md"
    
    # 格式化内容
    content = f"""# Antigravity 会话记录

**会话 ID**: {timestamp}
**保存时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**保存者**: Executive (Antigravity AI)

---

## AI 自动摘要

{ai_summary}

---

## 元数据
- 生成方式: AI 自动总结
- 目的: 跨会话记忆延续
- 下次会话: 新窗口 AI 可直接读取此摘要

---

*此文件由 AI 会话记忆系统自动生成*
"""
    
    # n8n webhook 配置
    webhook_url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"
    payload = {
        "owner": "baifan7574",
        "repo": "grich-cloud",
        "path": f"CONVERSATION_HISTORY/{filename}",
        "content": content,
        "message": f"AI Auto-save: {timestamp}"
    }
    
    try:
        print(f"\n📝 AI 正在保存会话记录到 GitHub...")
        print(f"文件路径: CONVERSATION_HISTORY/{filename}")
        
        response = requests.post(webhook_url, json=payload, timeout=15)
        
        if response.status_code == 200:
            print("\n✅ 会话记录保存成功!")
            print(f"\n📂 GitHub 路径:")
            print(f"   https://github.com/baifan7574/grich-cloud/blob/main/CONVERSATION_HISTORY/{filename}")
            print(f"\n💡 新窗口使用方法:")
            print(f'   直接对 AI 说: "读取上次会话记忆"')
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
    print("    🤖 AI 智能会话保存系统")
    print("="*70)
    
    if len(sys.argv) > 1:
        # 从命令行参数读取 AI 摘要
        summary = " ".join(sys.argv[1:])
    else:
        print("\n⚠️ 使用方法:")
        print("python save_ai_summary.py \"AI生成的摘要内容\"")
        print("\n提示: 这个脚本应该由 AI 调用,而不是手动运行")
        sys.exit(1)
    
    # 保存到 GitHub
    success = save_ai_summary_to_github(summary)
    
    print("\n" + "="*70)
    if success:
        print("✅ AI 会话记忆已保存!")
    else:
        print("⚠️ 保存可能未成功,请检查网络和 n8n 状态")
    print("="*70 + "\n")
    
    sys.exit(0 if success else 1)
