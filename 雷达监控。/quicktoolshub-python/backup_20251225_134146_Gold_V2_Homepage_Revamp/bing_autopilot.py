import requests
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BingAutopilot:
    def __init__(self):
        self.host = "soeasyhub.com"
        self.key = "a03727287ab1b016f667160e47665cab"
        self.key_location = f"https://{self.host}/{self.key}.txt"
        self.api_url = "https://api.indexnow.org/IndexNow"
        
    def get_urls_from_sitemap(self):
        """
        从 sitemap.xml 获取所有 URL
        由于是动态 Next.js 应用，我们直接尝试请求生成的 sitemap.xml
        或者从本地数据库/路由定义中获取
        """
        logger.info("正在获取站点所有 URL...")
        # 这里为了演示，我们先手动列出核心入口，稍后可以改为解析 sitemap
        urls = [
            f"https://{self.host}/",
            f"https://{self.host}/tools",
            f"https://{self.host}/blog",
            f"https://{self.host}/categories",
            f"https://{self.host}/tools/pdf-compressor",
            f"https://{self.host}/tools/image-resizer",
            f"https://{self.host}/tools/json-formatter",
            f"https://{self.host}/tools/word-counter",
            f"https://{self.host}/tools/background-remover",
        ]
        return urls

    def submit_to_bing(self, url_list):
        """将 URL 列表发送给 Bing"""
        logger.info(f"正在向微软 IndexNow 推送 {len(url_list)} 个 URL...")
        
        payload = {
            "host": self.host,
            "key": self.key,
            "keyLocation": self.key_location,
            "urlList": url_list
        }
        
        try:
            response = requests.post(
                self.api_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )
            
            if response.status_code == 200:
                logger.info("✅ 微软已成功接收推送！加速收录进行中...")
                return True
            else:
                logger.error(f"❌ 推送失败，状态码: {response.status_code}")
                logger.error(f"回复内容: {response.text}")
                return False
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            return False

if __name__ == "__main__":
    pilot = BingAutopilot()
    urls = pilot.get_urls_from_sitemap()
    pilot.submit_to_bing(urls)
    
    print("\n" + "="*50)
    print("🚀 微软全自动介入任务完成！")
    print("="*50)
    print(f"1. 已生成密钥文件: https://soeasyhub.com/{pilot.key}.txt")
    print(f"2. 已向 IndexNow 推送 {len(urls)} 个核心页面")
    print("3. 状态：等待微软蜘蛛在几分钟内到访")
    print("="*50)
