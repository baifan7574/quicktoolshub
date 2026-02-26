import os
import requests

# Fixed URL: replaced created_at with last_mined_at
url = "https://nbfzhxgkfljeuoncujum.supabase.co/rest/v1/grich_keywords_pool?is_refined=eq.true&select=slug,keyword,last_mined_at&limit=1"
anon_key = "sb_publishable_fXPwQ3q1K-shVTvskWv0Xw_vsQrhBoK"

def check_rls_with_anon_fixed():
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}"
    }
    
    print(f"Testing RLS with ANON key and CORRECT columns...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    check_rls_with_anon_fixed()
