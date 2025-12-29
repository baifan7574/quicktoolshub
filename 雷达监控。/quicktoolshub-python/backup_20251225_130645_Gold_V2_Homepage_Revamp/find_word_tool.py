from utils.supabase_client import get_supabase
import os

def find_word_tool():
    supabase = get_supabase()
    # If Supabase is mocked or unavailable, we might need another way, 
    # but let's try the real one if credentials allow.
    # Actually, the user's previous screenshot shows "Word Counter" in the list.
    try:
        result = supabase.table('tools').select('name, slug, id').ilike('name', '%Word%').execute()
        for tool in result.data:
            print(f"ID: {tool['id']}, Name: {tool['name']}, Slug: {tool['slug']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_word_tool()
