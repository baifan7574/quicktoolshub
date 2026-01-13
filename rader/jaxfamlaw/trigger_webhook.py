import requests
import json

url = "https://n8n.jaxfamlaw.com/webhook/gemini-update"
payload = {
    "owner": "baifan7574",
    "repo": "grich-cloud",
    "path": "SYSTEM_CHECK.md",
    "content": "Final Test: G-Drive Sync Verified by Executive at " + str(__import__('datetime').datetime.now()),
    "message": "G-Drive Sync Verification"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
