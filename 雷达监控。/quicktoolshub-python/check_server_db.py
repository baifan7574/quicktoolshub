import paramiko

def check_server_database():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    # 在服务器上运行 Python 脚本检查数据库
    check_script = """
import sys
sys.path.insert(0, '/root/soeasyhub_v2')
from utils.supabase_client import get_supabase

supabase = get_supabase()

if not supabase:
    print("ERROR: No Supabase connection")
    sys.exit(1)

# 检查分类
print("=== CATEGORIES ===")
categories = supabase.table('categories').select('*').execute()
for cat in categories.data:
    print(f"{cat['id']}: {cat['name']} ({cat['slug']})")

# 检查工具
print("\\n=== TOOLS ===")
tools = supabase.table('tools').select('*, categories(name)').eq('is_active', True).execute()
print(f"Total tools: {len(tools.data)}")
for tool in tools.data:
    cat_name = tool['categories']['name'] if tool.get('categories') else 'None'
    print(f"- {tool['name']} | Category: {cat_name} | Slug: {tool['slug']}")

# 统计每个分类的工具数
print("\\n=== TOOL COUNTS ===")
for cat in categories.data:
    count_result = supabase.table('tools').select('id', count='exact').eq('category_id', cat['id']).eq('is_active', True).execute()
    print(f"{cat['name']}: {count_result.count} tools")
"""
    
    cmd = f"cd /root/soeasyhub_v2 && python3 -c '{check_script}'"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    print("Server Database Check:")
    print("=" * 80)
    print(output)
    if error:
        print("\nErrors:")
        print(error)
    
    ssh.close()

if __name__ == "__main__":
    check_server_database()
