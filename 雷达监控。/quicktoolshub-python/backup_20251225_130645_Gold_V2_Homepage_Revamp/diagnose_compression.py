import paramiko

def diagnose_compression_issue():
    hostname = "43.130.229.184"
    username = "root"
    password = "baifan100100"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    
    commands = [
        # 查看最新的 gunicorn 日志
        "tail -100 /root/soeasyhub_v2/gunicorn.log",
        
        # 检查 uploads 目录
        "ls -lh /root/soeasyhub_v2/uploads/ | tail -20",
        
        # 手动测试 Ghostscript 压缩
        """cd /root/soeasyhub_v2/uploads && \
           if [ -f *.pdf ]; then \
               PDF_FILE=$(ls -t *.pdf | head -1); \
               echo "Testing compression on: $PDF_FILE"; \
               gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
                  -dNOPAUSE -dQUIET -dBATCH -sOutputFile=test_compressed.pdf "$PDF_FILE" 2>&1; \
               echo "Exit code: $?"; \
               ls -lh "$PDF_FILE" test_compressed.pdf 2>/dev/null; \
           else \
               echo "No PDF files found"; \
           fi""",
    ]
    
    for i, cmd in enumerate(commands):
        print(f"\n{'='*80}")
        print(f"Step {i+1}: {cmd[:60]}...")
        print('='*80)
        
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(output)
        if error:
            print(f"Error: {error}")
    
    ssh.close()

if __name__ == "__main__":
    diagnose_compression_issue()
