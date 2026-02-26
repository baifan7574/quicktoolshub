#!/usr/bin/env python3
"""
生产环境数据库审计脚本 - GRICH 项目
严格遵循宪法：使用 os.environ 读取 SUPABASE_URL 和 SUPABASE_KEY
连接 Supabase 数据库，查询 keywords 表，输出核心指标
"""

import os
from supabase import create_client

def main():
    print("🔍 GRICH 生产环境数据库审计")
    print("=" * 50)
    
    # 1. 从环境变量读取凭据（严格遵守宪法）
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ 环境变量缺失！")
        print("请设置以下环境变量：")
        print("  - SUPABASE_URL: Supabase 项目 URL")
        print("  - SUPABASE_KEY: Supabase anon/public key (非 SERVICE_ROLE_KEY)")
        print("\n当前环境变量：")
        print(f"  SUPABASE_URL = {supabase_url}")
        print(f"  SUPABASE_KEY = {'已设置' if supabase_key else '未设置'}")
        return
    
    print(f"✅ 使用环境变量连接 Supabase")
    print(f"   URL: {supabase_url[:30]}...")
    print(f"   KEY: {supabase_key[:10]}...")
    
    try:
        # 2. 创建 Supabase 客户端
        supabase = create_client(supabase_url, supabase_key)
        
        # 3. 查询总弹药量（Total Rows）
        total_res = supabase.table("keywords").select("id", count="exact").execute()
        total_rows = total_res.count
        
        # 4. 查询已生产文章（final_article 不为空）
        article_res = supabase.table("keywords").select("id", count="exact").not_.is_("final_article", "null").execute()
        article_count = article_res.count
        
        # 5. 查询已生产 PDF（pdf_url 不为空）
        pdf_res = supabase.table("keywords").select("id", count="exact").not_.is_("pdf_url", "null").execute()
        pdf_count = pdf_res.count
        
        # 6. 查询待命状态（is_downloaded 为 True）
        downloaded_res = supabase.table("keywords").select("id", count="exact").eq("is_downloaded", True).execute()
        downloaded_count = downloaded_res.count
        
        # 7. 输出结果
        print("\n📊 生产环境核心指标")
        print("=" * 50)
        print(f"总弹药量（关键词总数）: {total_rows:,}")
        print(f"已生产文章（final_article 不为空）: {article_count:,} ({article_count/total_rows*100:.1f}%)")
        print(f"已生产 PDF（pdf_url 不为空）: {pdf_count:,} ({pdf_count/total_rows*100:.1f}%)")
        print(f"待命状态（is_downloaded = True）: {downloaded_count:,} ({downloaded_count/total_rows*100:.1f}%)")
        
        # 8. 额外指标：计算生产漏斗
        print("\n🚀 生产漏斗分析")
        print("=" * 50)
        if total_rows > 0:
            print(f"📥 下载完成率: {downloaded_count/total_rows*100:.1f}%")
            if downloaded_count > 0:
                # 假设 refined 字段存在
                try:
                    refined_res = supabase.table("keywords").select("id", count="exact").eq("is_refined", True).execute()
                    refined_count = refined_res.count
                    print(f"🔧 精炼完成率: {refined_count/downloaded_count*100:.1f}%")
                except:
                    pass
            print(f"📝 文章生产率: {article_count/total_rows*100:.1f}%")
            print(f"📄 PDF 生成率: {pdf_count/article_count*100:.1f}%" if article_count > 0 else "📄 PDF 生成率: 0.0%")
        
        # 9. 样本检查
        print("\n🔬 样本检查")
        print("=" * 50)
        sample = supabase.table("keywords").select("slug, keyword, final_article, pdf_url, is_downloaded").limit(3).execute()
        if sample.data:
            for i, item in enumerate(sample.data, 1):
                status = []
                if item.get("final_article"): status.append("文章✓")
                if item.get("pdf_url"): status.append("PDF✓")
                if item.get("is_downloaded"): status.append("下载✓")
                print(f"{i}. {item['slug'][:40]}... | {item['keyword'][:30]}... | {' '.join(status)}")
        
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")
        print("\n💡 可能的原因：")
        print("1. 表名不正确（应该是 'keywords' 还是 'grich_keywords_pool'？）")
        print("2. RLS 策略限制")
        print("3. 网络连接问题")
        
        # 尝试使用 grich_keywords_pool 表（已知的表格名）
        print("\n🔄 尝试使用 'grich_keywords_pool' 表...")
        try:
            supabase = create_client(supabase_url, supabase_key)
            test_res = supabase.table("grich_keywords_pool").select("id", count="exact").limit(1).execute()
            print(f"✅ 发现 'grich_keywords_pool' 表，包含 {test_res.count} 行记录")
            print("请修改脚本中的表名为 'grich_keywords_pool'")
        except Exception as e2:
            print(f"❌ 'grich_keywords_pool' 表也不存在: {e2}")

if __name__ == "__main__":
    main()