import paramiko

HOST = "43.130.229.184"
USER = "root"
PW = "baifan100100"

def remote_check():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        client.connect(HOST, username=USER, password=PW)
        
        commands = [
            "curl -sb -o /dev/null -w '%{http_code}' http://localhost:9999/tools/alternative-to-best-regards",
            "curl -s http://localhost:9999/tools/alternative-to-best-regards | grep 'Communication Pro Engine' | head -n 1"
        ]
        
        for cmd in commands:
            print(f"\nRunning: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            print(f"Result: {stdout.read().decode().strip()}")
            
    except Exception as e:
        print(f"SSH Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    remote_check()
