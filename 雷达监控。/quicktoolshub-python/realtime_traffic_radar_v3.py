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

    async def check_connectivity_status(self):
        """检查各外部服务的真实连接状态"""
        status_report = {'bing': '❌', 'clarity': '❌', 'google': '❌'}
        try:
            # 检查 Bing
            r_bing = requests.get("https://soeasyhub.com/a03727287ab1b016f667160e47665cab.txt", timeout=2)
            if "a03727287ab1b016f667160e47665cab" in r_bing.text: status_report['bing'] = '✅'
            
            # 检查网站 & Clarity (从首页源码找)
            r_home = requests.get("https://soeasyhub.com/", timeout=2)
            if "clarity" in r_home.text.lower() and "uqdwtqfbf6" in r_home.text: status_report['clarity'] = '✅'
            if "googletagmanager" in r_home.text.lower(): status_report['google'] = '✅'
        except: pass
        return status_report

    def start(self):
        print(f"\n{'='*120}")
        print("🚀 SoEasyHub 流量雷达 V3.1 - 「全能指挥官版」已启动")
        print(f"👤 人类 | 🔍 谷歌 | Ⓜ️ 必应 | 🚫 恶意探测 | 🤖 机器人")
        print(f"监控中心：Google/Bing 收录探测 | 热力图状态报告 | 全球 IP 画像")
        print(f"{'='*120}\n")
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            ssh.get_transport().set_keepalive(30)
            
            stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 -f {self.log_path}")
            
            header = f"{'时间':<10} | {'属性及类型':<14} | {'动作':<5} | {'来源地/Referer':<20} | {'目标路径及意图'}"
            print(header)
            print("-" * 125)
            
            count = 0
            for line in stdout:
                if line.strip():
                    self.process(line)
                    count += 1
                    if count % 10 == 0:
                        self.print_summary()
        except Exception as e:
            print(f"❌ 链路中断: {e}")
            time.sleep(5)
            self.start()

    def print_summary(self):
        # 实时获取连接状态
        import asyncio
        conn = {'bing': '⏳', 'clarity': '⏳', 'google': '⏳'}
        try:
            # 简易同步版检测
            r = requests.get("https://soeasyhub.com/", timeout=1)
            conn['bing'] = '✅' if "a03727287" in r.text or requests.get("https://soeasyhub.com/a03727287ab1b016f667160e47665cab.txt", timeout=1).status_code == 200 else '❌'
            conn['clarity'] = '✅' if "clarity" in r.text.lower() else '❌'
            conn['google'] = '✅' if "googletagmanager" in r.text.lower() else '❌'
        except: pass

        print(f"\n{'#'*35} 📡 全局连通性监控 {'#'*35}")
        print(f"🌐 站点在线: ✅ | Ⓜ️ Bing验证: {conn['bing']} | 🔥 Clarity录制: {conn['clarity']} | 🔍 Google监控: {conn['google']}")
        print(f"{'#'*30} 📊 流量实时汇总 (累计) {'#'*30}")
        print(f"👥 总量: {self.stats['total']} | 👤 真人: {self.stats['human']} | 🕵️ 搜索蜘蛛: {self.stats['bot']} | 🚫 拦截: {self.stats['malicious']}")
        print(f"🌍 活跃国家: {', '.join([f'{c}({n})' for c,n in self.stats['countries'].most_common(3)])}")
        print(f"💰 累计转化: {self.stats['conversions']} 次工具调用 | 🔝 热门工具: {self.stats['tools'].most_common(1)[0][0] if self.stats['tools'] else '暂无'}")
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
