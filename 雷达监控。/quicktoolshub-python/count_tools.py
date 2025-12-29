from utils.supabase_client import get_supabase

supabase = get_supabase()
result = supabase.table('tools').select('name, slug, is_active').execute()

print(f'总工具数: {len(result.data)}')
print('\n已激活的工具:')
for t in result.data:
    if t.get('is_active'):
        print(f"  - {t['name']} ({t['slug']})")

active_count = len([t for t in result.data if t.get('is_active')])
print(f'\n已激活工具总数: {active_count}')
