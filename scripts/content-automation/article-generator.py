#!/usr/bin/env python3
"""
文章生成器
功能：使用AI生成SEO优化的文章内容
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 尝试导入AI库
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

load_dotenv()

class ArticleGenerator:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('AI_MODEL', 'gpt-4o-mini')
        self.default_length = int(os.getenv('DEFAULT_ARTICLE_LENGTH', 1500))
        
        # 初始化AI客户端
        if self.openai_key and OPENAI_AVAILABLE:
            self.ai_client = OpenAI(api_key=self.openai_key)
            self.ai_provider = 'openai'
        elif self.anthropic_key and ANTHROPIC_AVAILABLE:
            self.ai_client = anthropic.Anthropic(api_key=self.anthropic_key)
            self.ai_provider = 'anthropic'
        else:
            raise ValueError("需要配置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
    
    def generate_slug(self, title: str) -> str:
        """生成URL友好的slug"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def generate_outline(self, keyword: str, article_type: str, target_tool: str = None) -> str:
        """生成文章大纲"""
        if article_type == 'how-to':
            prompt = f"""为关键词 "{keyword}" 创建一个详细的文章大纲。

文章类型：How-to教程
目标工具：{target_tool if target_tool else '通用'}

要求：
1. 包含清晰的步骤说明
2. 包含工具推荐部分
3. 包含常见问题解答
4. 包含最佳实践建议

请以Markdown格式输出大纲，包含：
- 标题
- 引言
- 主要步骤（至少5步）
- 工具推荐
- 常见问题
- 总结"""
        
        elif article_type == 'comparison':
            prompt = f"""为关键词 "{keyword}" 创建一个详细的文章大纲。

文章类型：对比文章

要求：
1. 对比不同工具/方法
2. 列出优缺点
3. 提供使用建议
4. 包含推荐

请以Markdown格式输出大纲。"""
        
        elif article_type == 'list':
            prompt = f"""为关键词 "{keyword}" 创建一个详细的文章大纲。

文章类型：列表文章

要求：
1. 列出10个最佳工具/方法
2. 每个工具包含简介、优缺点、使用场景
3. 包含总结和推荐

请以Markdown格式输出大纲。"""
        
        else:  # question
            prompt = f"""为关键词 "{keyword}" 创建一个详细的文章大纲。

文章类型：问题解答

要求：
1. 直接回答问题
2. 提供详细解释
3. 包含相关工具推荐
4. 包含实际案例

请以Markdown格式输出大纲。"""
        
        return self._call_ai(prompt)
    
    def generate_article(self, keyword: str, outline: str, article_type: str, 
                        target_tool: str = None, word_count: int = None) -> str:
        """生成完整文章"""
        word_count = word_count or self.default_length
        
        prompt = f"""根据以下大纲，写一篇关于 "{keyword}" 的完整文章。

文章类型：{article_type}
目标字数：{word_count}字
目标工具：{target_tool if target_tool else '通用'}

大纲：
{outline}

要求：
1. 文章必须完整、详细、有价值
2. 自然融入关键词（不要堆砌）
3. 包含实际使用步骤和示例
4. 如果提到工具，请使用自然的方式推荐
5. 使用Markdown格式
6. 包含标题、段落、列表等
7. 确保文章长度达到目标字数

请直接输出文章内容，不要包含其他说明。"""
        
        return self._call_ai(prompt)
    
    def generate_title(self, keyword: str, article_type: str) -> str:
        """生成SEO优化的标题"""
        prompt = f"""为关键词 "{keyword}" 生成一个SEO优化的文章标题。

文章类型：{article_type}

要求：
1. 标题必须包含关键词
2. 标题长度：50-60字符
3. 标题要有吸引力
4. 可以包含年份（2024）
5. 可以包含"Free"、"Complete Guide"等词

只输出标题，不要其他内容。"""
        
        title = self._call_ai(prompt).strip()
        # 清理标题
        title = re.sub(r'^["\']|["\']$', '', title)
        return title
    
    def generate_excerpt(self, content: str, max_length: int = 155) -> str:
        """从文章内容生成摘要"""
        # 提取第一段或前几句话
        paragraphs = content.split('\n\n')
        excerpt = paragraphs[0] if paragraphs else content[:200]
        
        # 清理Markdown标记
        excerpt = re.sub(r'#+\s*', '', excerpt)
        excerpt = re.sub(r'\*\*([^*]+)\*\*', r'\1', excerpt)
        excerpt = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', excerpt)
        
        # 截断到合适长度
        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length].rsplit(' ', 1)[0] + '...'
        
        return excerpt.strip()
    
    def _call_ai(self, prompt: str) -> str:
        """调用AI API"""
        if self.ai_provider == 'openai':
            response = self.ai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的SEO内容写作专家，擅长写高质量、SEO友好的技术文章。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        
        elif self.ai_provider == 'anthropic':
            response = self.ai_client.messages.create(
                model=self.model if 'claude' in self.model else 'claude-3-haiku-20240307',
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    
    def generate(self, keyword_data: dict) -> dict:
        """生成完整文章数据"""
        keyword = keyword_data['keyword']
        article_type = keyword_data.get('article_type', 'how-to')
        target_tool = keyword_data.get('target_tool')
        
        print(f"📝 生成文章: {keyword}")
        
        # 1. 生成标题
        print("   生成标题...")
        title = self.generate_title(keyword, article_type)
        
        # 2. 生成大纲
        print("   生成大纲...")
        outline = self.generate_outline(keyword, article_type, target_tool)
        
        # 3. 生成文章
        print("   生成文章内容...")
        content = self.generate_article(keyword, outline, article_type, target_tool)
        
        # 4. 生成摘要
        excerpt = self.generate_excerpt(content)
        
        # 5. 生成slug
        slug = self.generate_slug(title)
        
        # 6. 计算阅读时长（假设每分钟200字）
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)
        
        # 7. 提取标签
        tags = self._extract_tags(keyword, article_type, target_tool)
        
        result = {
            'title': title,
            'slug': slug,
            'excerpt': excerpt,
            'content': content,
            'category': keyword_data.get('category'),
            'tags': tags,
            'keywords': [keyword],
            'related_tools': [target_tool] if target_tool else [],
            'reading_time': reading_time,
            'word_count': word_count,
            'article_type': article_type,
            'status': 'generated',
            'created_at': datetime.now().isoformat()
        }
        
        print(f"✅ 文章生成完成！")
        print(f"   标题: {title}")
        print(f"   字数: {word_count}")
        print(f"   阅读时长: {reading_time}分钟")
        
        return result
    
    def _extract_tags(self, keyword: str, article_type: str, target_tool: str = None) -> list:
        """提取标签"""
        tags = []
        
        # 从关键词提取
        if 'pdf' in keyword.lower():
            tags.append('PDF')
        if 'image' in keyword.lower() or 'photo' in keyword.lower():
            tags.append('Image')
        if 'free' in keyword.lower():
            tags.append('Free')
        if 'online' in keyword.lower():
            tags.append('Online')
        
        # 文章类型标签
        tags.append(article_type.replace('-', ' ').title())
        
        # 工具标签
        if target_tool:
            tags.append(target_tool.replace('-', ' ').title())
        
        return list(set(tags))  # 去重


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python article-generator.py <关键词JSON文件> [输出目录]")
        print("示例: python article-generator.py ../data/keywords-processed.json ../data/articles-generated/")
        sys.exit(1)
    
    generator = ArticleGenerator()
    input_file = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('../data/articles-generated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取关键词
    with open(input_file, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
    
    # 生成文章（示例：前5个）
    print(f"🚀 开始生成文章...")
    for i, keyword_data in enumerate(keywords[:5], 1):
        print(f"\n[{i}/{min(5, len(keywords))}]")
        try:
            article = generator.generate(keyword_data)
            
            # 保存文章
            output_file = output_dir / f"{article['slug']}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            
            print(f"💾 保存文章: {output_file}")
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            continue
    
    print(f"\n✅ 完成！")

