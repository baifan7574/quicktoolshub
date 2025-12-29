import paramiko
import time
import re
from datetime import datetime

class RealtimeTrafficRadarV2_1:
    """
    SoEasyHub 流量雷达 V2.1 - 视觉加固版
    """
    def __init__(self):
        self.hostname = "43.130.229.184"
        self.username = "root"
        self.password = "baifan100100"
        self.log_path = "/var/log/nginx/access.log"

    def start(self):
        print(f"\n{'='*80}")
        print("🚀 SoEasyHub 流量雷达 V2.1 - 「视觉指挥官版」已就绪")
        print(f"🛡️ 蓝色盾牌 = 安全访问 | 🔥 火焰 = 赚钱页面 | 🔍/Ⓜ️ = 顶级搜索蜘蛛")
        print(f"{'='*80}\n")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            
            # 开启心跳保活，防止长时间无流量导致断连
            ssh.get_transport().set_keepalive(30)
            
            stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 -f {self.log_path}")
            
            print(f"{'时间':<10} | {'状态及类型':<12} | {'访客来源':<15} | {'目标页面':<40}")
            print("-" * 100)
            
            for line in stdout:
                self.process(line)
        except Exception as e:
            print(f"❌ 错误: {e}")

    def process(self, line):
        try:
            ip = line.split(' ')[0]
            request_match = re.search(r'"(GET|POST) (.*?) HTTP', line)
            url = request_match.group(2) if request_match else "Unknown"
            if any(ext in url for ext in ['.css', '.js', '.png', '.jpg', '_next']): return

            user_agent = line.split('"')[-2]
            icon = "🛡️ 安全访客"
            if "Googlebot" in user_agent: icon = "🔍 谷歌搜索"
            elif "Bingbot" in user_agent: icon = "Ⓜ️ 必应搜索"
            elif "bot" in user_agent.lower(): icon = "🤖 机器人"

            money_flag = "🔥 " if any(kw in url.lower() for kw in ['pdf', 'image', 'tools', 'convert']) else ""
            
            # Parse time from Nginx log like [24/Dec/2025:16:09:58 +0800]
            time_match = re.search(r':(\d{2}:\d{2}:\d{2})', line)
            time_str = time_match.group(1) if time_match else "刚刚"

            print(f"{time_str:<10} | {icon:<12} | {ip:<15} | {money_flag}{url}")
        except: pass

if __name__ == "__main__":
    RealtimeTrafficRadarV2_1().start()
