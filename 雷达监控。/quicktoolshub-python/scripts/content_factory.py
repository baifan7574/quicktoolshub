
import os
import sys
import random
import datetime
from dotenv import load_dotenv

# 添加父目录到路径以便导入 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import get_supabase

# 加载环境变量
load_dotenv()

class ContentFactory:
    """
    SEO 自动化内容工厂 - 专为 SoEasyHub 定制
    结合 '专家视角 + 焦虑SEO' 策略
    """
    def __init__(self):
        self.supabase = get_supabase()
        
    def generate_expert_identity(self):
        """定义专家身份 Prompt"""
        identities = [
            "作为一名执业10年的合同法律师",
            "根据我5年的心理咨询临床经验",
            "从人力资源总监(HRD)的视角来看",
            "作为一名每天处理上百份教案的资深教师"
        ]
        return random.choice(identities)

    def generate_pain_point(self):
        """生成焦虑/痛点"""
        pain_points = [
            {"title": "为什么你的邮件总被已读不回？", "tool": "pdf-compressor", "angle": "职场社交礼仪"},
            {"title": "一张不合规的图片可能让你赔偿十万", "tool": "background-remover", "angle": "法律合规风险"},
            {"title": "机械性重复劳动正在由于摧毁你的创造力", "tool": "pdf-to-word", "angle": "职业倦怠心理"},
            {"title": "为什么发截图给客户是非常不专业的行为？", "tool": "image-to-pdf", "angle": "信任构建"},
        ]
        return random.choice(pain_points)

    def generate_article_content(self, identity, pain_point):
        """
        生成文章内容 (目前是模板化生成，可接入 LLM)
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 模拟深度文章结构
        content = f"""
## {identity}，我想和你谈谈：{pain_point['title']}

在我的职业生涯中，我见过太多优秀的人才因为忽略了微小的细节而错失机会。今天我们要聊的不是技术，而是**{pain_point['angle']}**。

### 1. 那些被你忽视的“隐形扣分项”
当你把一个 25MB 的 PDF 合同直接扔给客户时，你传递的信息不仅仅是文件本身，还有一种“我不在这对方时间”的傲慢。
从心理学角度来看，这会立即触发接收者的防御机制（Defense Mechanism）。

### 2. 这里的风险比你想象的要大
如果是图片版权问题，这就更严重了。很多时候，我们以为“随便搜张图”能用，殊不知背景里的某个商标可能就构成了侵权。
这就是为什么我总是强调：**专业人士必须使用干净、合规的素材**。

### 3. 如何低成本解决这个问题？
你不需要花钱雇人，也不需要购买昂贵的软件。
我们的 **{pain_point['tool']}** 工具就是为此而生的。

*   **痛点**：{pain_point['title']}
*   **解药**：使用 QuickToolsHub 的自动化工具
*   **成本**：0元，0注册

### 专家建议
{identity}，我建议你现在就检查一下你最近发出的五个文件。如果有问题，立刻使用我们的工具进行修正。这不仅是工作习惯，更是职业修养。

> *本文由 QuickToolsHub 专家团队生成于 {today}，旨在提升您的职场竞争力。*
        """
        return content

    def run(self):
        print("🚀 content_factory 正在启动...")
        
        # 1. 构思选题
        identity = self.generate_expert_identity()
        pain_point = self.generate_pain_point()
        
        title = f"{pain_point['title']} - {identity}的深度建议"
        slug = f"expert-advice-{random.randint(1000,9999)}"
        
        print(f"📝 正在撰写文章: {title}")
        content = self.generate_article_content(identity, pain_point)
        
        # 2. 存入数据库
        article_data = {
            "title": title,
            "slug": slug,
            "content": content,
            "excerpt": f"{identity}，深度解析{pain_point['angle']}...",
            "is_published": True,
            "published_at": datetime.datetime.now().isoformat(),
            "category": "Expert Advice",
            "tags": [pain_point['tool'], "职场提升", "专家观点"]
        }
        
        try:
            # 这里的 supabase.table 需要根据您实际表结构调整
            # 假设表名是 'articles'
            self.supabase.table('articles').insert(article_data).execute()
            print("✅ 文章已成功发布到数据库！")
            
            # TODO: 自动 Ping Google Sitemap
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            print("(提示：可能是因为数据库表结构不匹配，或者 Supabase Key 未配置)")

if __name__ == "__main__":
    factory = ContentFactory()
    factory.run()
