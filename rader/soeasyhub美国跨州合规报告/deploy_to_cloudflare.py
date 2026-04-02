import os
import subprocess

def load_config():
    config = {}
    token_path = os.path.join(".agent", "Token..txt")
    with open(token_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "CLOUDFLARE_EMAIL:" in line: config['email'] = line.split("EMAIL:")[1].strip()
            if "CLOUDFLARE_API_KEY:" in line: config['key'] = line.split("KEY:")[1].strip()
    return config

def main():
    config = load_config()
    os.environ['CLOUDFLARE_API_TOKEN'] = config['key']
    os.environ['CLOUDFLARE_EMAIL'] = config['email']
    
    print("Deploying soeasyhub-v2 to Cloudflare...")
    # Run wrangler publish in the subdirectory
    cmd = "npx wrangler deploy"
    result = subprocess.run(cmd, shell=True, cwd="soeasyhub-v2", capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        print("Deployment Successful!")
        print(result.stdout)
    else:
        print("Deployment Failed.")
        print(result.stderr)
        print(result.stdout)

if __name__ == "__main__":
    main()
