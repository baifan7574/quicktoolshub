from utils.supabase_client import get_supabase
import json

def list_db_tools():
    supabase = get_supabase()
    result = supabase.table('tools').select('name, slug, id').execute()
    for tool in result.data:
        print(f"ID: {tool['id']}, Name: {tool['name']}, Slug: {tool['slug']}")

if __name__ == "__main__":
    list_db_tools()
