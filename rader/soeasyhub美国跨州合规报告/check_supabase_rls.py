import os
import requests

url = "https://nbfzhxgkfljeuoncujum.supabase.co/rest/v1/grich_keywords_pool?is_refined=eq.true&select=slug,keyword,last_mined_at&limit=1"
# The anon key (Publishable key) from Token..txt
anon_key = "sb_publishable_fXPwQ3q1K-shVTvskWv0Xw_vsQrhBoK"

def check_rls_with_anon():
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}"
    }
    
    print(f"Testing RLS with ANON key...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ RLS is likely OFF or SELECT is allowed for ANON.")
        elif response.status_code in [401, 403]:
            print("❌ RLS error! Permission denied for ANON key.")
        else:
            print(f"❓ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    check_rls_with_anon()
