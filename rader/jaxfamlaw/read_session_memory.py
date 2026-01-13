"""
会话记忆读取工具
从 GitHub 仓库读取历史会话记录
"""
import sys
import requests

def list_all_sessions():
    """列出所有保存的会话记录"""
    api_url = "https://api.github.com/repos/baifan7574/grich-cloud/contents/CONVERSATION_HISTORY"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            files = response.json()
            if isinstance(files, list):
                print("\n📚 历史会话记录列表:\n")
                for idx, file in enumerate(files, 1):
                    if file['name'].endswith('.md'):
                        print(f"{idx}. {file['name']}")
                        print(f"   大小: {file['size']} bytes")
                        print(f"   链接: {file['html_url']}\n")
                return [f['name'] for f in files if f['name'].endswith('.md')]
            else:
                print("⚠️ CONVERSATION_HISTORY 文件夹为空或格式异常")
                return []
        elif response.status_code == 404:
            print("⚠️ CONVERSATION_HISTORY 文件夹不存在，还没有保存过会话记录")
            return []
        else:
            print(f"❌ 获取文件列表失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 错误: {e}")
        return []

def read_session(filename):
    """读取指定会话记录"""
    base_url = "https://raw.githubusercontent.com/baifan7574/grich-cloud/main/CONVERSATION_HISTORY"
    url = f"{base_url}/{filename}"
    
    try:
        print(f"\n📖 正在读取会话记录: {filename}")
        response = requests.get(url)
        
        if response.status_code == 200:
            print("\n" + "="*70)
            print(response.text)
            print("="*70)
            return response.text
        else:
            print(f"\n❌ 读取失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return None

def read_latest_session():
    """读取最新的会话记录"""
    sessions = list_all_sessions()
    if sessions:
        latest = sorted(sessions, reverse=True)[0]
        print(f"\n📌 最新会话: {latest}")
        return read_session(latest)
    else:
        print("\n⚠️ 没有找到历史会话记录")
        return None

if __name__ == "__main__":
    print("\n" + "="*70)
    print("    📖 Antigravity 会话记忆读取系统")
    print("="*70)
    
    if len(sys.argv) > 1:
        # 读取指定文件
        filename = sys.argv[1]
        if not filename.endswith('.md'):
            filename += '.md'
        read_session(filename)
    else:
        # 交互模式
        print("\n选择操作:")
        print("1. 查看所有会话记录")
        print("2. 读取最新会话")
        print("3. 读取指定会话")
        
        choice = input("\n请选择 (1/2/3): ").strip()
        
        if choice == '1':
            list_all_sessions()
        elif choice == '2':
            read_latest_session()
        elif choice == '3':
            sessions = list_all_sessions()
            if sessions:
                filename = input("\n输入文件名: ").strip()
                if not filename.endswith('.md'):
                    filename += '.md'
                read_session(filename)
        else:
            print("❌ 无效选择")
    
    print("\n" + "="*70 + "\n")
