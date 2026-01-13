import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print(f"CWD: {os.getcwd()}")
print("Listing files in CWD:")
try:
    for f in os.listdir('.'):
        print(f" - {f!r}")  # Use repr to show hidden chars
except Exception as e:
    print(f"Error listing dir: {e}")

target = "DAILY_LOG.md"
print(f"\nAttempting to read {target}...")
if os.path.exists(target):
    try:
        with open(target, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print(f"File {target} NOT found in CWD.")
