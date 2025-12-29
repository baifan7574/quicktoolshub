import paramiko
import time
import re
from datetime import datetime

class RealtimeTrafficRadarV2_2:
    """
    SoEasyHub 流量雷达 V2.2 - 决策情报版
    """
    def __init__(self):
        self.hostname = "43.130.229.184"
        self.username = "root"
        self.password = "baifan100100"
        self.log_path = "/var/log/nginx/access.log"
        
        # 恶意探测路径库
        self.malicious_paths = [
            '.php', '/wp-', '/admin', '/solr', '/cgi-bin', '/config', '/.env', 
            '/xmlrpc', '/HNAP1', '/actuator', '/evox', '/sdk', '/v2/_catalog'
        ]

    def start(self):
        print(f"\n{'='*100}")
        print("🚀 SoEasyHub 流量雷达 V2.2 - 「战略级情报控制台」已启动")
        print(f"👤 真实人类 = 浏览器访客 | 🔍/Ⓜ️ = 优质蜘蛛 | 🤖 爬虫脚本 = 爬数据 | 🚫 恶意探测 = 全自动攻击扫描")
        print(f"🔥 火焰 = 核心赚钱工具 | 📄 博客 = 潜在流量入口")
        print(f"{'='*100}\n")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            
            # 开启心跳保活
            ssh.get_transport().set_keepalive(30)
            
            # 实时读取日志尾部
            stdin, stdout, stderr = ssh.exec_command(f"tail -n 30 -f {self.log_path}")
            
            header = f"{'时间':<10} | {'属性及类型':<14} | {'动作':<5} | {'来源地/Referer':<20} | {'目标路径及意图'}"
            print(header)
            print("-" * 120)
            
            for line in stdout:
                if line.strip():
                    self.process(line)
        except Exception as e:
            print(f"❌ 链路中断: {e}")
            print("正在尝试重连...")
            time.sleep(5)
            self.start()

    def process(self, line):
        try:
            # 1. 提取 IP
            ip = line.split(' ')[0]
            
            # 2. 提取请求方法和 URL
            request_match = re.search(r'"(GET|POST|HEAD|PUT) (.*?) HTTP', line)
            if not request_match: return
            method = request_match.group(1)
            url = request_match.group(2)
            
            # 过滤噪声（静态资源）
            if any(ext in url.lower() for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.woff', '_next', '/static/']):
                return

            # 3. 提取 Referer (来源)
            parts = line.split('"')
            referer = parts[3] if len(parts) > 3 else "-"
            referer_short = referer.replace("https://", "").replace("http://", "").split('/')[0]
            if referer_short == "soeasyhub.com": referer_short = "站内跳转"
            elif referer_short == "-": referer_short = "直接访问"

            # 4. 提取 User-Agent 并判断身份
            user_agent = parts[5] if len(parts) > 5 else "-"
            
            # 身份判定逻辑
            icon = "👤 真实人类"
            low_ua = user_agent.lower()
            
            # 判定搜索机器人
            if "googlebot" in low_ua: icon = "🔍 谷歌蜘蛛"
            elif "bingbot" in low_ua: icon = "Ⓜ️ 必应蜘蛛"
            elif "baiduspider" in low_ua: icon = "🇨🇳 百度蜘蛛"
            elif "yandexbot" in low_ua: icon = "🇷🇺 Yandex"
            # 判定恶意或探测脚本
            elif any(p in url.lower() for p in self.malicious_paths):
                icon = "🚫 恶意探测"
            # 判定普通爬虫
            elif "bot" in low_ua or "spider" in low_ua or "crawler" in low_ua:
                icon = "🤖 自动爬虫"
            # 判定真实人类（带常见浏览器特征）
            elif "mozilla" in low_ua and ("chrome" in low_ua or "safari" in low_ua or "firefox" in low_ua):
                icon = "👤 真实人类"
            else:
                icon = "⚙️ 未知进程"

            # 5. 目标页面意图识别
            money_flag = ""
            if any(kw in url.lower() for kw in ['pdf', 'image', 'background', 'remover', 'compress', 'resize']):
                money_flag = "🔥 [赚钱工具] "
            elif url.startswith('/blog/'):
                money_flag = "📄 [内容引流] "
            elif url == "/":
                money_flag = "🏠 [门户进入] "
            elif url == "/tools":
                money_flag = "🗃️ [工具大厅] "
            
            # 6. 提取时间
            time_match = re.search(r':(\d{2}:\d{2}:\d{2})', line)
            time_str = time_match.group(1) if time_match else "刚刚"

            # 7. 格式化输出
            print(f"{time_str:<10} | {icon:<14} | {method:<5} | {referer_short[:20]:<20} | {money_flag}{url}")
            
        except Exception as e:
            # print(f"DEBUG Error: {e}") # 生产环境保持静默
            pass

if __name__ == "__main__":
    RealtimeTrafficRadarV2_2().start()
