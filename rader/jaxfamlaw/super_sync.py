import os
import sys
import json
import datetime
import subprocess

LOG_FILE = r"d:\quicktoolshub\雷达监控。\GRICH\n8n_exec.log"
GDRIVE_PATH = r"G:\我的云端硬盘\GRICH_AI_BRAIN\GRICH_MASTER_LOG.md"
REPO_DIR = r"d:\quicktoolshub\雷达监控。\GRICH\grich-astro"

def log_status(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()}: [SUPER_SYNC] {msg}\n")

def run_git_commands(path, content, message):
    try:
        # 1. 写入文件
        full_path = os.path.join(REPO_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 2. Git 操作
        # 使用 shell=True 因为在 Windows 上更可靠
        cmds = [
            ["git", "add", "."],
            ["git", "commit", "-m", message],
            ["git", "push"]
        ]
        for c in cmds:
            res = subprocess.run(c, cwd=REPO_DIR, capture_output=True, text=True, encoding='utf-8')
            if res.returncode != 0 and "nothing to commit" not in res.stderr:
                log_status(f"Git Cmd Failed: {' '.join(c)} -> {res.stderr}")
            else:
                log_status(f"Git Cmd Success: {' '.join(c)}")
        return True
    except Exception as e:
        log_status(f"Git Sync Error: {e}")
        return False

def run_gdrive_sync(content):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n--- {timestamp} ---\n{content}\n"
        with open(GDRIVE_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
        log_status(f"G-Drive Sync Success: {len(content)} chars.")
        return True
    except Exception as e:
        log_status(f"G-Drive Sync Error: {e}")
        return False

if __name__ == "__main__":
    try:
        # 允许从命令行参数读取 JSON 文件，或者从 stdin 读取
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                raw_input = f.read().strip()
            log_status(f"Read payload from file: {sys.argv[1]}")
        else:
            raw_input = sys.stdin.read().strip()
            log_status("Read payload from stdin.")
            
        if not raw_input:
            log_status("Error: No input received.")
            sys.exit(1)
            
        data = json.loads(raw_input)
        # 支持两种结构：一种是直接 body，一种是 n8n 的 $json 包装
        body = data.get("body", data)
        
        owner = body.get("owner")
        repo = body.get("repo")
        path = body.get("path")
        content = body.get("content")
        message = body.get("message", "Auto Memory Sync")

        if not content:
            log_status("Error: No content found in JSON.")
            sys.exit(1)

        # 执行双重同步
        run_gdrive_sync(content)
        if path:
            run_git_commands(path, content, message)
            
        print("SYNC_COMPLETE")
    except Exception as e:
        log_status(f"Main Entry Error: {e}")
        sys.exit(1)
