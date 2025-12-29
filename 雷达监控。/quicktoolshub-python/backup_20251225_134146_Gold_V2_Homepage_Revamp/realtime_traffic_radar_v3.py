import paramiko
import time
import re
import requests
from datetime import datetime
from collections import Counter

class RealtimeTrafficRadarV3:
    """
    SoEasyHub 流量雷达 V3.0 - 商业情报与转化分析版
    """
    def __init__(self):
        self.hostname = "43.130.229.184"
        self.username = "root"
        self.password = "baifan100100"
        self.log_path = "/var/log/nginx/access.log"
        
        # 恶意探测路径
        self.malicious_paths = [
            '.php', '/wp-', '/admin', '/solr', '/cgi-bin', '/config', '/.env', 
            '/xmlrpc', '/HNAP1', '/actuator', '/evox', '/sdk', '/v2/_catalog', '.git/'
        ]
        
        # 统计数据
        self.stats = {
            'total': 0,
            'human': 0,
            'bot': 0,
            'malicious': 0,
            'conversions': 0, # 工具使用次数 (POST /api)
            'ips': set(),
            'countries': Counter(),
            'tools': Counter()
        }
        
        # 本地持久化存储路径 (黑匣子)
        self.history_file = "d:/quicktoolshub/quicktoolshub-python/traffic_history.csv"
        self._init_history()
        
        # IP 地理位置缓存
        self.geo_cache = {}

    def _init_history(self):
        """初始化持久化记录文件"""
        import os
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write("timestamp,type,ip,country,device,intent,url\n")

    def save_event(self, data):
        """保存关键事件到本地历史记录"""
        try:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                line = f"{data['time']},{data['type']},{data['ip']},{data['country']},{data['device']},{data['intent']},{data['url']}\n"
                f.write(line)
        except: pass

    def get_geo(self, ip):
        if ip in self.geo_cache:
            return self.geo_cache[ip]
        try:
            # 使用 ip-api.com (免费额度 45次/分)
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,countryCode", timeout=2)
            if r.status_code == 200 and r.json().get('status') == 'success':
                country = r.json().get('countryCode', '??')
                self.geo_cache[ip] = country
                return country
        except: pass
        return "??"

    def start(self):
        print(f"\n{'='*120}")
        print("🚀 SoEasyHub 流量雷达 V3.0 - 「商业情报指挥部」已启动")
        print(f"👤 人类 | 🔍 蜘蛛 | 🤖 机器人 | 🚫 恶意探测 | 📱/💻 设备")
        print(f"统计指标：流量汇总 / 地理画像 / 工具转化率 / 恶意过滤")
        print(f"{'='*120}\n")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            ssh.get_transport().set_keepalive(30)
            
            stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 -f {self.log_path}")
            
            header = f"{'时间':<10} | {'类型':<12} | {'设备':<4} | {'IP (国家)':<22} | {'来源':<15} | {'深度意图与路径'}"
            print(header)
            print("-" * 125)
            
            count = 0
            for line in stdout:
                if line.strip():
                    self.process(line)
                    count += 1
                    # 每 10 条日志显示一次汇总报告
                    if count % 10 == 0:
                        self.print_summary()
        except Exception as e:
            print(f"❌ 通讯中断: {e}")
            time.sleep(5)
            self.start()

    def print_summary(self):
        print(f"\n{'#'*35} ⚡ 实时运营简报 {'#'*35}")
        print(f"📊 总请求: {self.stats['total']} | 👤 真人: {self.stats['human']} | 🕵️ 蜘蛛: {self.stats['bot']} | 🚫 拦截: {self.stats['malicious']}")
        print(f"🌍 覆盖国家: {', '.join([f'{c}({n})' for c,n in self.stats['countries'].most_common(5)])}")
        print(f"🔥 工具排行: {', '.join([f'{t}({n})' for t,n in self.stats['tools'].most_common(3)])}")
        conv_rate = (self.stats['conversions'] / max(1, self.stats['human'])) * 100
        print(f"💰 转化效率 (累计): {self.stats['conversions']} 次工具使用 (约 {conv_rate:.1f}% 转化率)")
        print(f"{'#'*86}\n")

    def process(self, line):
        try:
            self.stats['total'] += 1
            parts = line.split('"')
            
            # 1. IP & Country
            ip = line.split(' ')[0]
            self.stats['ips'].add(ip)
            country = self.get_geo(ip)
            self.stats['countries'][country] += 1
            ip_display = f"{ip} ({country})"

            # 2. Method & URL
            request_match = re.search(r'"(GET|POST|HEAD) (.*?) HTTP', line)
            if not request_match: return
            method = request_match.group(1)
            url = request_match.group(2)
            
            if any(ext in url.lower() for ext in ['.css', '.js', '.png', '.jpg', '.svg', '.woff', '_next', '/static/']):
                return

            # 3. User-Agent & Device
            ua = parts[5] if len(parts) > 5 else "-"
            ua_lower = ua.lower()
            
            device = "💻"
            if "mobile" in ua_lower or "android" in ua_lower or "iphone" in ua_lower:
                device = "📱"

            # 4. Identity & Attributes
            icon = "👤 真实人类"
            if "googlebot" in ua_lower:
                icon = "🔍 谷歌蜘蛛"; self.stats['bot'] += 1
            elif "bingbot" in ua_lower:
                icon = "Ⓜ️ 必应蜘蛛"; self.stats['bot'] += 1
            elif any(p in url.lower() for p in self.malicious_paths):
                icon = "🚫 恶意探测"; self.stats['malicious'] += 1
            elif "bot" in ua_lower or "spider" in ua_lower or "crawler" in ua_lower:
                icon = "🤖 自动网络"; self.stats['bot'] += 1
            else:
                icon = "👤 真实人类"; self.stats['human'] += 1

            # 5. Conversion Tracking (POST to API)
            intent = ""
            if method == "POST" and "/api/convert" in url:
                self.stats['conversions'] += 1
                intent = "💰 [用户在使用工具!] "
            elif any(kw in url.lower() for kw in ['pdf', 'image', 'background', 'remover', 'compress']):
                self.stats['tools'][url.split('/')[-1]] += 1
                intent = "🔥 [高意向页面] "
            elif "/blog/" in url:
                intent = "📄 [内容引流] "
            
            # 6. Referer
            referer = parts[3] if len(parts) > 3 else "-"
            ref_short = referer.split('/')[2] if '//' in referer else "直接访问"
            if "soeasyhub.com" in ref_short: ref_short = "站内"

            # 7. Time
            time_match = re.search(r':(\d{2}:\d{2}:\d{2})', line)
            time_str = time_match.group(1) if time_match else "--:--:--"

            # 7. 保存到本地 (持久化)
            self.save_event({
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': icon,
                'ip': ip,
                'country': country,
                'device': device,
                'intent': intent.strip() if intent else "浏览",
                'url': url
            })

            print(f"{time_str:<10} | {icon:<10} | {device:<4} | {ip_display:<22} | {ref_short[:15]:<15} | {intent}{url}")
        except: pass

if __name__ == "__main__":
    RealtimeTrafficRadarV3().start()
