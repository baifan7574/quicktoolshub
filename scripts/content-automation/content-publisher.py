#!/usr/bin/env python3
"""
内容发布器
功能：将生成的文章发布到Supabase数据库
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from supabase import create_client, Client

load_dotenv()

class ContentPublisher:
    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("需要配置 SUPABASE_URL 和 SUPABASE_SERVICE_KEY")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def publish_article(self, article_data: dict, publish_now: bool = False) -> dict:
        """发布单篇文章"""
        # 准备文章数据
        article = {
            'title': article_data['title'],
            'slug': article_data['slug'],
            'excerpt': article_data.get('excerpt'),
            'content': article_data['content'],
            'category': article_data.get('category'),
            'tags': article_data.get('tags', []),
            'reading_time': article_data.get('reading_time'),
            'is_published': publish_now,
            'published_at': datetime.now().isoformat() if publish_now else None,
        }
        
        # 检查slug是否已存在
        existing = self.supabase.table('articles').select('id').eq('slug', article['slug']).execute()
        if existing.data:
            print(f"⚠️  文章已存在: {article['slug']}")
            return {'status': 'exists', 'id': existing.data[0]['id']}
        
        # 插入文章
        result = self.supabase.table('articles').insert(article).execute()
        
        if result.data:
            article_id = result.data[0]['id']
            print(f"✅ 文章发布成功: {article['title']} (ID: {article_id})")
            
            # 关联工具
            if article_data.get('related_tools'):
                self._link_tools(article_id, article_data['related_tools'])
            
            return {'status': 'success', 'id': article_id}
        else:
            print(f"❌ 文章发布失败: {article['title']}")
            return {'status': 'error'}
    
    def _link_tools(self, article_id: int, tool_slugs: list):
        """关联工具到文章"""
        for tool_slug in tool_slugs:
            # 查找工具ID
            tool_result = self.supabase.table('tools').select('id').eq('slug', tool_slug).execute()
            
            if tool_result.data:
                tool_id = tool_result.data[0]['id']
                
                # 检查关联是否已存在
                existing = self.supabase.table('tool_articles').select('id').eq('article_id', article_id).eq('tool_id', tool_id).execute()
                
                if not existing.data:
                    # 创建关联
                    self.supabase.table('tool_articles').insert({
                        'tool_id': tool_id,
                        'article_id': article_id,
                        'relation_type': 'tutorial'
                    }).execute()
                    print(f"   ✅ 关联工具: {tool_slug}")
            else:
                print(f"   ⚠️  工具不存在: {tool_slug}")
    
    def schedule_publish(self, article_id: int, publish_date: datetime):
        """安排定时发布"""
        self.supabase.table('articles').update({
            'published_at': publish_date.isoformat(),
            'is_published': False
        }).eq('id', article_id).execute()
        
        print(f"📅 安排发布: {publish_date.strftime('%Y-%m-%d %H:%M')}")
    
    def batch_publish(self, articles_dir: str, publish_now: bool = False, 
                     daily_limit: int = 2, start_date: datetime = None):
        """批量发布文章"""
        articles_path = Path(articles_dir)
        if not articles_path.exists():
            raise ValueError(f"目录不存在: {articles_dir}")
        
        # 获取所有文章文件
        article_files = list(articles_path.glob('*.json'))
        print(f"📚 找到 {len(article_files)} 篇文章")
        
        if not article_files:
            return
        
        # 确定发布日期
        if start_date is None:
            start_date = datetime.now()
        
        published_count = 0
        scheduled_count = 0
        
        for i, article_file in enumerate(article_files, 1):
            print(f"\n[{i}/{len(article_files)}] 处理: {article_file.name}")
            
            # 读取文章数据
            with open(article_file, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
            
            # 决定是否立即发布
            should_publish_now = publish_now and published_count < daily_limit
            
            # 发布文章
            result = self.publish_article(article_data, should_publish_now)
            
            if result['status'] == 'success':
                if should_publish_now:
                    published_count += 1
                else:
                    # 安排定时发布
                    publish_date = start_date + timedelta(days=scheduled_count // daily_limit)
                    self.schedule_publish(result['id'], publish_date)
                    scheduled_count += 1
        
        print(f"\n✅ 批量发布完成！")
        print(f"   立即发布: {published_count} 篇")
        print(f"   定时发布: {scheduled_count} 篇")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python content-publisher.py <文章目录> [选项]")
        print("选项:")
        print("  --publish-now    立即发布（前2篇）")
        print("  --schedule        定时发布（每天2篇）")
        print("示例: python content-publisher.py ../data/articles-generated/ --schedule")
        sys.exit(1)
    
    publisher = ContentPublisher()
    articles_dir = sys.argv[1]
    publish_now = '--publish-now' in sys.argv
    schedule = '--schedule' in sys.argv or not publish_now
    
    publisher.batch_publish(articles_dir, publish_now=publish_now, schedule=schedule)

