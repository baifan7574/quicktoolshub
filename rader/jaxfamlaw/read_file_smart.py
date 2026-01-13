import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

cwd_files = os.listdir('.')
print(f"Scanned {len(cwd_files)} files.")

targets = ["DAILY_LOG", "PHASE2", "TECH_EXECUTION"]

for target_keyword in targets:
    print(f"\n--- Searching for {target_keyword} ---")
    found_name = None
    for f in cwd_files:
        if target_keyword in f and f.endswith(".md"):
            found_name = f
            break
            
    if found_name:
        print(f"Found match: {found_name!r}")
        try:
            with open(found_name, "r", encoding="utf-8") as f_obj:
                content = f_obj.read()
                print(f"HEAD content:\n{content[:500]}")
                print("...\n[END HEAD]")
        except Exception as e:
            print(f"Error reading {found_name}: {e}")
    else:
        print("No matching file found.")
