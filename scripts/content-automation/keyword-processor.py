#!/usr/bin/env python3
"""
关键词处理器
功能：处理从Google Keyword Planner等工具拉取的关键词数据
"""

import pandas as pd
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class KeywordProcessor:
    def __init__(self):
        self.min_volume = int(os.getenv('MIN_SEARCH_VOLUME', 100))
        self.max_volume = int(os.getenv('MAX_SEARCH_VOLUME', 5000))
        self.max_competition = os.getenv('MAX_COMPETITION', 'medium')
        
        # 工具关键词映射
        self.tool_keywords = {
            'pdf-merger': ['merge pdf', 'combine pdf', 'pdf merger'],
            'pdf-splitter': ['split pdf', 'divide pdf', 'pdf splitter'],
            'pdf-compressor': ['compress pdf', 'reduce pdf size', 'pdf compressor'],
            'pdf-to-word': ['pdf to word', 'convert pdf to word', 'pdf word converter'],
            'image-compressor': ['compress image', 'reduce image size', 'image optimizer'],
            'image-resizer': ['resize image', 'change image size', 'image resizer'],
            'image-converter': ['convert image', 'image format converter', 'change image format'],
            'background-remover': ['remove background', 'transparent background', 'background remover'],
            'word-counter': ['word counter', 'count words', 'character counter'],
            'text-case-converter': ['text case converter', 'uppercase lowercase', 'text transformer'],
            'lorem-ipsum-generator': ['lorem ipsum', 'placeholder text', 'dummy text'],
            'json-formatter': ['json formatter', 'format json', 'json beautifier'],
            'base64-encoder': ['base64 encode', 'base64 decoder', 'base64 converter'],
            'url-encoder': ['url encode', 'url decoder', 'url encoder'],
        }
        
        # 文章类型判断规则
        self.article_type_patterns = {
            'how-to': ['how to', 'how do', 'tutorial', 'guide', 'step by step'],
            'comparison': ['vs', 'versus', 'compare', 'comparison', 'difference'],
            'list': ['best', 'top', '10', '5', 'list', 'review'],
            'question': ['what is', 'why', 'when', 'where', 'can i', 'should i'],
        }
    
    def load_keywords(self, file_path: str) -> pd.DataFrame:
        """加载关键词文件（CSV或JSON）"""
        file_path = Path(file_path)
        
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")
        
        return df
    
    def filter_keywords(self, df: pd.DataFrame) -> pd.DataFrame:
        """筛选有效关键词"""
        # 确保必要的列存在
        required_columns = ['keyword', 'search_volume', 'competition']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"缺少必要的列: {missing_columns}")
        
        # 筛选规则
        filtered = df[
            (df['search_volume'] >= self.min_volume) &
            (df['search_volume'] <= self.max_volume) &
            (df['competition'].isin(['low', 'medium']))
        ].copy()
        
        return filtered
    
    def classify_keyword(self, keyword: str) -> dict:
        """分类关键词：文章类型、目标工具"""
        keyword_lower = keyword.lower()
        
        # 判断文章类型
        article_type = 'how-to'  # 默认
        for type_name, patterns in self.article_type_patterns.items():
            if any(pattern in keyword_lower for pattern in patterns):
                article_type = type_name
                break
        
        # 匹配目标工具
        target_tool = None
        for tool_slug, keywords_list in self.tool_keywords.items():
            if any(kw in keyword_lower for kw in keywords_list):
                target_tool = tool_slug
                break
        
        # 判断分类
        category = None
        if 'pdf' in keyword_lower:
            category = 'PDF Tools'
        elif 'image' in keyword_lower or 'photo' in keyword_lower:
            category = 'Image Tools'
        elif 'text' in keyword_lower or 'word' in keyword_lower:
            category = 'Text Tools'
        elif 'json' in keyword_lower or 'code' in keyword_lower or 'developer' in keyword_lower:
            category = 'Developer Tools'
        
        return {
            'article_type': article_type,
            'target_tool': target_tool,
            'category': category
        }
    
    def calculate_priority(self, row: pd.Series) -> float:
        """计算关键词优先级"""
        # 优先级 = 搜索量 / 竞争度系数
        competition_scores = {'low': 1.0, 'medium': 0.7, 'high': 0.3}
        competition_score = competition_scores.get(row['competition'], 0.5)
        
        priority = row['search_volume'] * competition_score
        
        # 如果有工具匹配，提高优先级
        classification = self.classify_keyword(row['keyword'])
        if classification['target_tool']:
            priority *= 1.2
        
        return priority
    
    def process(self, input_file: str, output_file: str = None) -> pd.DataFrame:
        """处理关键词：加载、筛选、分类、排序"""
        print(f"📥 加载关键词文件: {input_file}")
        df = self.load_keywords(input_file)
        print(f"   原始关键词数量: {len(df)}")
        
        print(f"🔍 筛选关键词...")
        df_filtered = self.filter_keywords(df)
        print(f"   筛选后数量: {len(df_filtered)}")
        
        print(f"🏷️ 分类关键词...")
        classifications = df_filtered['keyword'].apply(self.classify_keyword)
        df_filtered['article_type'] = classifications.apply(lambda x: x['article_type'])
        df_filtered['target_tool'] = classifications.apply(lambda x: x['target_tool'])
        df_filtered['category'] = classifications.apply(lambda x: x['category'])
        
        print(f"📊 计算优先级...")
        df_filtered['priority'] = df_filtered.apply(self.calculate_priority, axis=1)
        
        # 按优先级排序
        df_filtered = df_filtered.sort_values('priority', ascending=False)
        
        # 添加状态列
        df_filtered['status'] = 'pending'
        
        # 保存结果
        if output_file:
            output_path = Path(output_file)
            if output_path.suffix == '.csv':
                df_filtered.to_csv(output_file, index=False)
            elif output_path.suffix == '.json':
                df_filtered.to_json(output_file, orient='records', indent=2)
            print(f"💾 保存处理结果: {output_file}")
        
        print(f"✅ 处理完成！")
        print(f"   最终关键词数量: {len(df_filtered)}")
        print(f"   文章类型分布:")
        print(df_filtered['article_type'].value_counts().to_string())
        
        return df_filtered


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python keyword-processor.py <输入文件> [输出文件]")
        print("示例: python keyword-processor.py ../data/keywords-raw.csv ../data/keywords-processed.json")
        sys.exit(1)
    
    processor = KeywordProcessor()
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = processor.process(input_file, output_file)
    print("\n前10个高优先级关键词:")
    print(result[['keyword', 'search_volume', 'competition', 'priority', 'article_type', 'target_tool']].head(10).to_string())

