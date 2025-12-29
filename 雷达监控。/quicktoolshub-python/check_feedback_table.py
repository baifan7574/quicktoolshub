from utils.supabase_client import get_supabase
import json

def check_table():
    supabase = get_supabase()
    if not supabase:
        print("Supabase not configured.")
        return

    print("Checking 'user_feedback' table...")
    try:
        # Try a sample select
        result = supabase.table('user_feedback').select('*').limit(1).execute()
        print("Success! Table exists. Data:", result.data)
    except Exception as e:
        print(f"Error: {e}")
        print("Attempting to insert a sample record to confirm existence...")
        try:
            insert_result = supabase.table('user_feedback').insert({
                'type': 'test',
                'content': 'Check if table exists',
                'status': 'pending'
            })
            print("Successfully inserted sample record!")
        except Exception as e2:
            print(f"Insert failed: {e2}")
            print("\nIMPORTANT: Please ensure the 'user_feedback' table is created in Supabase with these columns:")
            print("- id (uuid/int, PK)")
            print("- created_at (timestamp)")
            print("- type (text)")
            print("- content (text)")
            print("- tool_slug (text, nullable)")
            print("- contact (text, nullable)")
            print("- status (text)")

if __name__ == "__main__":
    check_table()
