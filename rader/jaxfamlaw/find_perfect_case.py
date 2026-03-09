import os
import requests

# Supabase Config
URL = "https://rdlmumybuwveaaeceohj.supabase.co/rest/v1"
KEY = "sb_publishable_aPXWTauRxJ88A88mwLDoPQ_puVi7PZj"
HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}"
}

def find_perfect_case():
    print("Searching for perfect case example...")
    
    # 1. 先找有被告记录的案号
    res_def = requests.get(f"{URL}/defendants?select=case_number,defendant_name&limit=10", headers=HEADERS)
    defendants = res_def.json()
    
    if not defendants:
        print("No defendant records found in DB.")
        return

    # 2. 对比这些案号在 lawsuits 表中的情况
    for d in defendants:
        case_no = d['case_number']
        # 尝试精准匹配或模糊匹配
        res_law = requests.get(f"{URL}/lawsuits?case_number=eq.{case_no}&select=*", headers=HEADERS)
        lawsuits = res_law.json()
        
        if lawsuits:
            l = lawsuits[0]
            # 检查关键字段是否完整
            is_perfect = (
                l.get('plaintiff') and l.get('plaintiff') != 'Unknown' and
                l.get('court') and l.get('court') != 'Unknown'
            )
            
            if is_perfect:
                print(f"\nFound a relatively perfect case:")
                print(f"Case No: {case_no}")
                print(f"Plaintiff: {l.get('plaintiff')}")
                print(f"Defendant: {d['defendant_name']}")
                print(f"URL: https://jaxfamlaw.com/case_template?case={case_no}&defendant={d['defendant_name']}")
                return

    # 3. 如果没找到完全重合的，随机给一个有基础信息的
    print("\nNo direct match for Case+Defendant, showing an available case:")
    res_any = requests.get(f"{URL}/lawsuits?select=*&limit=1", headers=HEADERS)
    l = res_any.json()[0]
    print(f"Case No: {l['case_number']}")
    print(f"Plaintiff: {l['plaintiff']}")
    print(f"URL: https://jaxfamlaw.com/case_template?case={l['case_number']}")

if __name__ == "__main__":
    find_perfect_case()
