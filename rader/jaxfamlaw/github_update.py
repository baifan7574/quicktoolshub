import requests
import json
import sys
import os
import datetime

# 这里的 Token 是从 n8n 里的凭证中提取的（假设环境中有，或者我们通过命令行传递，为了安全，我们改用从参数读取）
# 考虑到 n8n 的 executeCommand 可以传环境或参数，我们在这里统一使用脚本逻辑。
# 虽然可以使用 local git，但为了保持与 n8n 配置一致，我们还是用 API，但脚本会先 GET 获取 SHA。

def log_msg(msg):
    with open(r"d:\quicktoolshub\雷达监控。\GRICH\n8n_exec.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()}: [GITHUB] {msg}\n")

def perform_update(owner, repo, path, content, message, token):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. 获取现有文件的 SHA
    sha = None
    try:
        r = requests.get(api_url, headers=headers)
        if r.status_code == 200:
            sha = r.json().get('sha')
            log_msg(f"Found existing file {path}, SHA: {sha}")
    except Exception as e:
        log_msg(f"Error checking file: {e}")

    # 2. 执行更新
    payload = {
        "message": message,
        "content": __import__('base64').b64encode(content.encode('utf-8')).decode('utf-8')
    }
    if sha:
        payload["sha"] = sha

    try:
        r = requests.put(api_url, headers=headers, json=payload)
        if r.status_code in [200, 201]:
            log_msg(f"Successfully updated {path} on GitHub.")
            return True
        else:
            log_msg(f"GitHub Error ({r.status_code}): {r.text}")
            return False
    except Exception as e:
        log_msg(f"Exception during update: {e}")
        return False

if __name__ == "__main__":
    # 参数顺序: owner, repo, path, content_file, message, token
    if len(sys.argv) < 7:
        print("Usage: python github_update.py <owner> <repo> <path> <content_file> <message> <token>")
        sys.exit(1)

    owner, repo, path, content_file, message, token = sys.argv[1:7]
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if perform_update(owner, repo, path, content, message, token):
            print("SUCCESS")
        else:
            print("FAILED")
            sys.exit(1)
    except Exception as e:
        log_msg(f"Main error: {e}")
        sys.exit(1)
