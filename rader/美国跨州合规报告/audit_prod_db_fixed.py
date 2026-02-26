#!/usr/bin/env python3
"""
生产环境数据库审计脚本 - 真实摸底
严格遵守宪法：优先使用 os.environ 读取 SUPABASE_URL 和 SUPABASE_KEY
若环境变量未设置，则从 Token..txt 读取作为后备
连接 Supabase 数据库，查询 grich_keywords_pool 表
输出核心指标的真实计数
"""

import os
import sys
from supabase import create_client

def load_credentials():
    """加载 Supabase 凭据，优先使用环境变量"""
    # 1. 优先使用环境变量（严格遵守宪法）
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        print("[INFO] 使用环境变量凭据")
        return supabase_url, supabase_key
    
    # 2. 后备：从 Token..txt 读取
    print("[WARN] 环境变量未设置，使用 Token..txt 作为后备")
    token_paths = [
        ".agent/Token..txt",
        os.path.join(".agent", "Token..txt"),
        r"d:\quicktoolshub\rader\美国跨州合规报告\.agent\Token..txt"
    ]
    
    for token_path in token_paths:
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    url = None
                    key = None
                    for line in content.split('\n'):
                        if 'Project URL:' in line:
                            url = line.split('Project URL:')[1].strip()
                        if 'Secret keys:' in line:
                            key = line.split('Secret keys:')[1].strip()
                    if url and key:
                        print(f"[INFO] 从 {token_path} 读取凭据")
                        return url, key
            except Exception as e:
                print(f"[ERROR] 读取 {token_path} 失败: {e}")
    
    # 3. 如果都没有找到，抛出异常（禁止硬编码密钥）
    raise ValueError(
        "未找到 Supabase 凭据。请设置环境变量 SUPABASE_URL 和 SUPABASE_KEY，或创建 .agent/Token..txt 文件。"
        "禁止在代码中硬编码密钥！"
    )

def audit_database():
    """执行数据库审计"""
    print("=" * 60)
    print("GRICH 生产环境数据库审计 - 真实摸底")
    print("=" * 60)
    
    # 加载凭据
    supabase_url, supabase_key = load_credentials()
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase KEY: {supabase_key[:15]}...")
    print("-" * 60)
    
    try:
        # 创建客户端
        supabase = create_client(supabase_url, supabase_key)
        
        # 1. 总弹药量：有多少个关键词 (Total Rows)
        print("\n[1] 查询总弹药量...")
        total_res = supabase.table("grich_keywords_pool").select("id", count="exact").execute()
        total_rows = total_res.count
        print(f"   总关键词数: {total_rows:,}")
        
        # 2. 已生产文章：final_article 字段不为空的有多少？
        print("\n[2] 查询已生产文章...")
        article_res = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("final_article", "null").execute()
        article_count = article_res.count
        print(f"   final_article 不为空: {article_count:,}")
        
        # 3. 已生产 PDF：pdf_url 字段不为空的有多少？
        print("\n[3] 查询已生产 PDF...")
        pdf_res = supabase.table("grich_keywords_pool").select("id", count="exact").not_.is_("pdf_url", "null").execute()
        pdf_count = pdf_res.count
        print(f"   pdf_url 不为空: {pdf_count:,}")
        
        # 4. 待命状态：is_downloaded 为 True 的有多少？
        print("\n[4] 查询待命状态...")
        downloaded_res = supabase.table("grich_keywords_pool").select("id", count="exact").eq("is_downloaded", True).execute()
        downloaded_count = downloaded_res.count
        print(f"   is_downloaded = True: {downloaded_count:,}")
        
        # 5. 其他有用指标
        print("\n[5] 其他生产指标...")
        # is_refined = True
        refined_res = supabase.table("grich_keywords_pool").select("id", count="exact").eq("is_refined", True).execute()
        refined_count = refined_res.count
        print(f"   is_refined = True: {refined_count:,}")
        
        # state 字段统计
        state_res = supabase.table("grich_keywords_pool").select("state", count="exact").execute()
        if hasattr(state_res, 'count'):
            print(f"   总记录数（通过state）: {state_res.count:,}")
        
        # 6. 输出汇总报告
        print("\n" + "=" * 60)
        print("📊 核心指标汇总报告")
        print("=" * 60)
        
        if total_rows > 0:
            print(f"1. 总弹药量（关键词总数）: {total_rows:,}")
            print(f"2. 已生产文章: {article_count:,} ({article_count/total_rows*100:.1f}%)")
            print(f"3. 已生产 PDF: {pdf_count:,} ({pdf_count/total_rows*100:.1f}%)")
            print(f"4. 待命状态（已下载）: {downloaded_count:,} ({downloaded_count/total_rows*100:.1f}%)")
            print(f"5. 数据精炼完成: {refined_count:,} ({refined_count/total_rows*100:.1f}%)")
            
            # 计算生产漏斗
            print("\n🚀 生产漏斗分析:")
            if downloaded_count > 0:
                print(f"   • 下载→精炼: {refined_count/downloaded_count*100:.1f}%")
            if refined_count > 0:
                print(f"   • 精炼→文章: {article_count/refined_count*100:.1f}%")
            if article_count > 0:
                print(f"   • 文章→PDF: {pdf_count/article_count*100:.1f}%")
            
            # 状态分布
            print("\n📈 状态分布（抽样）:")
            try:
                state_sample = supabase.table("grich_keywords_pool").select("state").limit(10).execute()
                states = {}
                for item in state_sample.data:
                    state = item.get('state', 'unknown')
                    states[state] = states.get(state, 0) + 1
                
                for state, count in states.items():
                    print(f"   • {state}: {count}")
            except:
                print("   • 无法获取状态分布")
        
        # 7. 样本检查
        print("\n" + "=" * 60)
        print("🔍 样本记录检查（前3条）")
        print("=" * 60)
        
        try:
            sample = supabase.table("grich_keywords_pool").select(
                "slug", "keyword", "final_article", "pdf_url", "is_downloaded", "is_refined"
            ).limit(3).execute()
            
            if sample.data:
                for i, item in enumerate(sample.data, 1):
                    slug = item.get('slug', 'N/A')[:40]
                    keyword = item.get('keyword', 'N/A')[:30]
                    has_article = "✓" if item.get('final_article') else "✗"
                    has_pdf = "✓" if item.get('pdf_url') else "✗"
                    is_dl = "✓" if item.get('is_downloaded') else "✗"
                    is_ref = "✓" if item.get('is_refined') else "✗"
                    
                    print(f"{i}. {slug}...")
                    print(f"   关键词: {keyword}...")
                    print(f"   状态: 文章{has_article} PDF{has_pdf} 下载{is_dl} 精炼{is_ref}")
                    print()
            else:
                print("数据库为空或无法获取样本")
        except Exception as e:
            print(f"样本检查失败: {e}")
            
        return {
            "total_rows": total_rows,
            "article_count": article_count,
            "pdf_count": pdf_count,
            "downloaded_count": downloaded_count,
            "refined_count": refined_count
        }
        
    except Exception as e:
        print(f"\n❌ 数据库连接或查询失败: {e}")
        print("\n可能的原因：")
        print("1. 网络连接问题")
        print("2. RLS（行级安全）策略限制")
        print("3. 表名不正确")
        print("4. 凭据无效")
        
        # 尝试诊断
        try:
            import requests
            test_url = f"{supabase_url}/rest/v1/"
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}"
            }
            response = requests.get(test_url, headers=headers, timeout=5)
            print(f"\nAPI 连接测试: {response.status_code}")
            if response.status_code == 200:
                print("Supabase API 可访问，可能是表名问题")
            else:
                print(f"API 返回错误: {response.text[:100]}")
        except Exception as e2:
            print(f"诊断失败: {e2}")
        
        return None

if __name__ == "__main__":
    # 设置编码以避免控制台编码问题
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    results = audit_database()
    
    print("\n" + "=" * 60)
    print("审计完成")
    print("=" * 60)
    
    if results:
        print("\n✅ 审计成功完成！")
        print(f"   数据库连接: 正常")
        print(f"   表名: grich_keywords_pool")
        print(f"   总记录: {results['total_rows']:,}")
    else:
        print("\n❌ 审计失败，请检查上述错误信息")