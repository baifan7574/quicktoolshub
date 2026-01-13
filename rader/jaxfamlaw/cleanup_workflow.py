import os

file_path = r"d:\quicktoolshub\.github\workflows\gbc-sniper.yml"

if os.path.exists(file_path):
    try:
        os.remove(file_path)
        print(f"Removed {file_path}")
    except Exception as e:
        print(f"Error removing file: {e}")
else:
    print("File not found.")
