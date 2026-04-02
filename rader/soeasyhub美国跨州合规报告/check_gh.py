import urllib.request
import json
import ssl
import zipfile
import io

def check_logs():
    run_id = '22535981638'  # Use the latest ID
    url = f'https://api.github.com/repos/baifan7574/soeasyhub-v2-main/actions/runs/{run_id}/logs'
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'python-urllib')
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                # Find the log file for 'Commit and Push Changes'
                for filename in z.namelist():
                    if 'Commit and Push Changes' in filename:
                        print(f"--- LOG FOR: {filename} ---")
                        content = z.read(filename).decode('utf-8', errors='replace')
                        lines = content.split('\n')
                        for line in lines[-20:]:
                            print(line)
                        print("-" * 40)
    except Exception as e:
        print('Error:', e)

check_logs()
