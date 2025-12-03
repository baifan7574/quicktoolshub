#!/usr/bin/env python3
"""
批量处理器
功能：完整的自动化流程 - 从关键词到发布
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from keyword_processor import KeywordProcessor
from article_generator import ArticleGenerator
from content_publisher import ContentPublisher
import json
import time

load_dotenv()

class BatchProcessor:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
        self.article_generator = ArticleGenerator()
        self.content_publisher = ContentPublisher()
        
        # 配置
        self.batch_size = 10  # 每批处理数量
        self.daily_limit = int(os.getenv('DEFAULT_ARTICLES_PER_DAY', 2))
    
    def process(self, keywords_file: str, output_dir: str = None, 
               max_articles: int = None, publish: bool = False):
        """完整处理流程"""
        output_dir = Path(output_dir) if output_dir else Path('../data')
        keywords_processed_dir = output_dir / 'keywords-processed'
        articles_dir = output_dir / 'articles-generated'
        
        keywords_processed_dir.mkdir(parents=True, exist_ok=True)
        articles_dir.mkdir(parents=True, exist_ok=True)
        
        print("=" * 60)
        print("🚀 开始批量处理流程")
        print("=" * 60)
        
        # 步骤1: 处理关键词
        print("\n📊 步骤1: 处理关键词")
        print("-" * 60)
        keywords_processed_file = keywords_processed_dir / 'keywords-processed.json'
        df_keywords = self.keyword_processor.process(
            keywords_file, 
            str(keywords_processed_file)
        )
        
        # 转换为字典列表
        keywords_list = df_keywords.to_dict('records')
        
        # 限制数量
        if max_articles:
            keywords_list = keywords_list[:max_articles]
        
        print(f"\n📝 步骤2: 生成文章 (共 {len(keywords_list)} 篇)")
        print("-" * 60)
        
        # 步骤2: 生成文章（分批处理）
        generated_count = 0
        failed_count = 0
        
        for i in range(0, len(keywords_list), self.batch_size):
            batch = keywords_list[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (len(keywords_list) + self.batch_size - 1) // self.batch_size
            
            print(f"\n📦 批次 {batch_num}/{total_batches} (共 {len(batch)} 个关键词)")
            
            for j, keyword_data in enumerate(batch, 1):
                keyword = keyword_data['keyword']
                print(f"\n[{j}/{len(batch)}] {keyword}")
                
                try:
                    # 生成文章
                    article = self.article_generator.generate(keyword_data)
                    
                    # 保存文章
                    article_file = articles_dir / f"{article['slug']}.json"
                    with open(article_file, 'w', encoding='utf-8') as f:
                        json.dump(article, f, ensure_ascii=False, indent=2)
                    
                    generated_count += 1
                    print(f"   ✅ 生成成功: {article_file.name}")
                    
                    # 避免API限流
                    time.sleep(2)
                    
                except Exception as e:
                    failed_count += 1
                    print(f"   ❌ 生成失败: {e}")
                    continue
            
            # 批次间休息
            if i + self.batch_size < len(keywords_list):
                print(f"\n⏸️  批次完成，休息10秒...")
                time.sleep(10)
        
        print(f"\n✅ 文章生成完成！")
        print(f"   成功: {generated_count} 篇")
        print(f"   失败: {failed_count} 篇")
        
        # 步骤3: 发布文章
        if publish and generated_count > 0:
            print(f"\n📤 步骤3: 发布文章")
            print("-" * 60)
            self.content_publisher.batch_publish(
                str(articles_dir),
                publish_now=False,  # 定时发布
                daily_limit=self.daily_limit
            )
        
        print("\n" + "=" * 60)
        print("🎉 批量处理完成！")
        print("=" * 60)
        print(f"\n📊 统计:")
        print(f"   处理关键词: {len(keywords_list)} 个")
        print(f"   生成文章: {generated_count} 篇")
        print(f"   发布文章: {'是' if publish else '否'}")
        
        if publish:
            print(f"\n📅 发布计划:")
            print(f"   每天发布: {self.daily_limit} 篇")
            total_days = (generated_count + self.daily_limit - 1) // self.daily_limit
            print(f"   预计完成: {total_days} 天")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python batch-processor.py <关键词文件> [选项]")
        print("选项:")
        print("  --max <数量>     最大生成文章数")
        print("  --publish        自动发布")
        print("  --output <目录>  输出目录")
        print("\n示例:")
        print("  python batch-processor.py ../data/keywords-raw.csv --max 50 --publish")
        sys.exit(1)
    
    processor = BatchProcessor()
    keywords_file = sys.argv[1]
    
    # 解析参数
    max_articles = None
    publish = False
    output_dir = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--max' and i + 1 < len(sys.argv):
            max_articles = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--publish':
            publish = True
            i += 1
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    processor.process(keywords_file, output_dir, max_articles, publish)

