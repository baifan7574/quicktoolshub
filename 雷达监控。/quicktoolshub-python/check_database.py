from utils.supabase_client import get_supabase

def check_database_tools():
    """检查数据库中的工具和分类"""
    supabase = get_supabase()
    
    if not supabase:
        print("❌ Supabase 连接失败")
        return
    
    print("=" * 80)
    print("检查数据库中的工具和分类")
    print("=" * 80)
    
    # 1. 检查所有分类
    print("\n[1] 所有分类:")
    try:
        categories = supabase.table('categories').select('*').execute()
        if categories.data:
            for cat in categories.data:
                print(f"  - {cat['name']} (slug: {cat['slug']}, id: {cat['id']})")
        else:
            print("  ❌ 没有分类数据")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 2. 检查所有工具
    print("\n[2] 所有工具:")
    try:
        tools = supabase.table('tools').select('*, categories(name, slug)').eq('is_active', True).execute()
        if tools.data:
            print(f"  总共 {len(tools.data)} 个工具:")
            for tool in tools.data:
                cat_name = tool['categories']['name'] if tool.get('categories') else 'No Category'
                print(f"  - {tool['name']} (slug: {tool['slug']}, category: {cat_name})")
        else:
            print("  ❌ 没有工具数据")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 3. 统计每个分类的工具数量
    print("\n[3] 每个分类的工具数量:")
    try:
        categories = supabase.table('categories').select('*').execute()
        if categories.data:
            for cat in categories.data:
                count_result = supabase.table('tools').select('id', count='exact').eq('category_id', cat['id']).eq('is_active', True).execute()
                count = count_result.count if count_result.count else 0
                print(f"  - {cat['name']}: {count} 个工具")
        else:
            print("  ❌ 没有分类数据")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

if __name__ == "__main__":
    check_database_tools()
