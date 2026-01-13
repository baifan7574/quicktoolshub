"""
执行官 → CTO 通信工具
发送消息到 CTO 并自动备份到 Google Drive
"""
import sys
import requests
from datetime import datetime

def send_to_cto(message):
    """发送消息到 CTO 并触发双线备份"""
    
    # 格式化消息
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📨 来自执行官的消息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

发送时间: {timestamp}
目标: CTO (Gemini)

消息内容:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
此消息已通过三角记忆回路自动备份:
✓ GitHub 仓库
✓ Google Drive 云盘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # n8n webhook 配置
    webhook_url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"
    payload = {
        "owner": "baifan7574",
        "repo": "grich-cloud",
        "path": "EXEC_TO_CTO_MESSAGES.md",
        "content": formatted_message,
        "message": f"Executive message at {timestamp}"
    }
    
    try:
        print("\n🚀 正在发送消息到 CTO...")
        print(f"📝 消息预览:\n{'-'*50}\n{message}\n{'-'*50}")
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("\n✅ 消息发送成功！")
            print("📊 执行结果:")
            print(f"   • Webhook 状态: {response.status_code}")
            print(f"   • 响应: {response.json().get('message', 'OK')}")
            print("\n📂 备份位置:")
            print("   1️⃣ GitHub: https://github.com/baifan7574/grich-cloud/blob/main/EXEC_TO_CTO_MESSAGES.md")
            print("   2️⃣ Google Drive: GRICH_AI_BRAIN/GRICH_MASTER_LOG.md")
            print("\n💡 提示:")
            print("   • GitHub 立即可见")
            print("   • Google Drive 云端同步需要 1-2 分钟")
            print("\n🔍 本地验证命令:")
            print('   Get-Content "G:\\我的云端硬盘\\GRICH_AI_BRAIN\\GRICH_MASTER_LOG.md" -Tail 20 -Encoding UTF8')
            
            return True
        else:
            print(f"\n❌ 发送失败: HTTP {response.status_code}")
            print(f"错误详情: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n⚠️ 请求超时，但消息可能已发送成功")
        print("请稍后查看 GitHub 或 Google Drive 确认")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("    📡 执行官 → CTO 通信系统")
    print("="*60)
    
    # 从命令行参数获取消息
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        print("\n请输入您要对 CTO 说的话 (输入完成后按 Enter):")
        print("-" * 60)
        message = input("➤ ")
    
    if not message.strip():
        print("\n❌ 消息不能为空！")
        sys.exit(1)
    
    # 发送消息
    success = send_to_cto(message)
    
    print("\n" + "="*60)
    if success:
        print("✅ 任务完成！消息已发送并备份")
    else:
        print("⚠️ 任务可能未完成，请检查网络连接")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
