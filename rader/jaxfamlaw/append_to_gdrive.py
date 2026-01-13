import sys
import os
from datetime import datetime

# 文件路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
status_log = os.path.join(current_dir, "n8n_exec.log")
gdrive_path = r"G:\我的云端硬盘\GRICH_AI_BRAIN\GRICH_MASTER_LOG.md"

def log_status(msg):
    with open(status_log, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: {msg}\n")

try:
    # 这里我们不再依赖命令行参数，而是让 n8n 在执行前把内容写到一个固定的临时文件
    # 读取内容：优先尝试从命令行参数指定的临时文件读取，否则从 stdin 读取
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                content = f.read()
            log_status(f"Read {len(content)} chars from file: {sys.argv[1]}")
        except Exception as e:
            log_status(f"Error reading file {sys.argv[1]}: {e}")
            content = sys.stdin.read()
            log_status(f"Fallback: Read {len(content)} chars from stdin due to file error.")
    else:
        content = sys.stdin.read()
        log_status(f"Read {len(content)} chars from stdin")
    
    content = content.strip() # Ensure content is stripped after reading from either source

    if not content:
        log_status("Warning: Received empty content from stdin or file")
        sys.exit(0)

    # 验证 G 盘
    if not os.path.exists(os.path.dirname(gdrive_path)):
        log_status(f"Error: G-Drive folder not found at {os.path.dirname(gdrive_path)}")
        sys.exit(1)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"\n--- {timestamp} ---\n{content}\n"

    with open(gdrive_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    log_status(f"Success: Appended {len(content)} chars to G-Drive")

except Exception as e:
    log_status(f"Exception: {str(e)}")
    sys.exit(1)
