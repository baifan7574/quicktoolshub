import paramiko
import time
import re
import sys

class RealtimeTrafficRadar:
    """
    SoEasyHub 实时流量雷达
    功能：实时监控服务器访问日志，显示谁在看您的网站。
    """
    def __init__(self):
        self.hostname = "43.130.229.184"
        self.username = "root"
        self.password = "baifan100100"
        self.log_path = "/var/log/nginx/access.log" # 假设使用 Nginx
        
    def start_monitoring(self):
        print(f"\n{'='*60}")
        print("🚀 SoEasyHub 实时流量雷达启动内容...")
        print(f"📡 正在连接远程服务器: {self.hostname}")
        print(f"{'='*60}\n")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            
            # 使用 tail -f 实时读取日志
            stdin, stdout, stderr = ssh.exec_command(f"tail -f {self.log_path}")
            
            print("🟢 连接成功！正在监听实时访问数据...\n")
            print(f"{'时间':<20} | {'IP地址':<15} | {'访问页面':<40}")
            print("-" * 80)
            
            for line in stdout:
                self.parse_and_display(line)
                
        except KeyboardInterrupt:
            print("\n\n🛑 雷达已手动关闭。")
            ssh.close()
        except Exception as e:
            print(f"\n❌ 连接失败: {str(e)}")
            print("💡 提示：如果 Nginx 日志路径不同，请联系指挥官修改路径。")

    def parse_and_display(self, log_line):
        """解析 Nginx 日志行"""
        # 典型的 Nginx 日志格式: 
        # 127.0.0.1 - - [24/Dec/2025:13:40:01 +0800] "GET /tools/pdf-compressor HTTP/1.1" 200 ...
        try:
            ip = log_line.split(' ')[0]
            # 提取访问的时间
            time_match = re.search(r'\[(.*?)\]', log_line)
            timestamp = time_match.group(1) if time_match else "Unknown"
            # 提取请求的 URL
            request_match = re.search(r'"(GET|POST) (.*?) HTTP', log_line)
            url = request_match.group(2) if request_match else "Unknown"
            
            # 过滤掉一些干扰（如静态资源）
            if not any(ext in url for ext in ['.css', '.js', '.png', '.jpg', '.svg', '.ico', '_next']):
                print(f"{timestamp:<20} | {ip:<15} | {url:<40}")
                
        except:
            pass # 捕获解析错误，不中断运行

if __name__ == "__main__":
    radar = RealtimeTrafficRadar()
    radar.start_monitoring()
