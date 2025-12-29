import requests
import sys

BASE_URL = "http://43.130.229.184:9999"

def check(url, must_contain, label):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"❌ {label}: Failed (Status {resp.status_code})")
            return False
        
        content = resp.text
        if must_contain in content:
            print(f"✅ {label}: Success (Found '{must_contain}')")
            return True
        else:
            print(f"❌ {label}: Content Missing! Page loaded but didn't find '{must_contain}'")
            # print(content[:500]) # Debug
            return False
    except Exception as e:
        print(f"❌ {label}: Error ({e})")
        return False

print("=== STARTING LIVE VERIFICATION ===")
# 1. Check Tool Page Layout
check(f"{BASE_URL}/tools/alternative-to-best-regards", "Communication Pro Engine", "Tool Page Header")
check(f"{BASE_URL}/tools/alternative-to-best-regards", "Sincerely", "Tool Page Content")

# 2. Check Blog Post
check(f"{BASE_URL}/blog/top-50-best-regards-alternatives-2025", "Times New Roman", "Blog Article")

# 3. Check Index List presence
check(f"{BASE_URL}/tools", "Alternative to Best Regards", "Index Page Listing")

# 4. Check Category Page
category_url = f"{BASE_URL}/tools?category=writing-assistant"
check(category_url, "Alternative to Best Regards", "Category Page - New Tool")
check(category_url, "Email Sign-Off Generator", "Category Page - Old Tool")

print("=== VERIFICATION COMPLETE ===")
