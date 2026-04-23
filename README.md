# Ransomware Simulation Lab

## Mô tả Dự án
Dự án này mô phỏng quá trình hoạt động của Ransomware trong môi trường mạng cô lập để nghiên cứu và giáo dục về an ninh mạng. Tất cả hoạt động được thực hiện trong máy ảo để đảm bảo an toàn.

## Mục đích (Purpose)
**Mục đích chỉ là nghiên cứu và giáo dục**

Dự án này được thiết kế hoàn toàn cho mục đích:
- **Nghiên cứu hành vi**: Quan sát và phân tích cách thức hoạt động của ransomware, từ lây nhiễm đến mã hóa dữ liệu.
- **Giáo dục an ninh mạng**: Giúp các chuyên gia an ninh hiểu rõ hơn về các mối đe dọa và cách bảo vệ hệ thống.
- **Đánh giá phòng chống**: Kiểm tra khả năng phòng chống và phát hiện của các công cụ bảo mật trong môi trường kiểm soát.

**Lưu ý quan trọng**: Tuyệt đối không sử dụng mã này hoặc kỹ thuật này cho bất kỳ mục đích xấu, tấn công hệ thống thực tế hoặc bất hợp pháp. Mọi hoạt động phải được thực hiện trong môi trường ảo hóa cô lập và với sự đồng ý của các bên liên quan.

## Yêu cầu Hệ thống
- Phần mềm ảo hóa: VirtualBox hoặc VMware.
- Máy chủ: Ít nhất 8GB RAM, 50GB dung lượng ổ cứng trống.

## Setup Môi trường Lab (Environment Setup)
Để thực hiện mô phỏng Ransomware một cách an toàn, hệ thống được triển khai trong môi trường mạng cô lập (Isolated Network) sử dụng ảo hóa.

### Cấu hình Máy ảo (Virtual Machines)
| Vai trò   | Hệ điều hành | Chức năng chính                          | Cấu hình đề nghị     |
|-----------|--------------|------------------------------------------|----------------------|
| Attacker  | Kali Linux  | Điều khiển (C2 Server), tạo payload, lắng nghe. | 4GB RAM, 20GB Disk |
| Victim    | Windows 10| Máy mục tiêu, thực thi mã độc, quan sát quá trình mã hóa. | 4GB RAM, 20GB Disk |

### Các bước thiết lập
1. **Cấu hình Mạng (Networking)**: Đặt cả hai máy ảo vào cùng một LAN Segment hoặc Host-only Adapter.

2. **Cấu hình máy Attacker (Kali Linux)**:
   - Cập nhật các công cụ cần thiết (wine, Python, hoặc các framework C2).

3. **Cấu hình máy Victim (Windows)**:
   - Tắt Windows Defender và Real-time Protection.
   - Tắt tường lửa (Firewall) nếu cần thiết để phục vụ việc demo kết nối ngược (Reverse Shell).

4. **Đóng gói mã độc (Packaging with Wine)**:
    - `sudo dpkg --add-architecture i386 && sudo apt update`  
      Sử dụng lệnh để hệ thống có thể nhận diện và cài đặt các thư viện 32-bit.
    - `sudo apt install wine32 wine64`  
      Cài đặt đồng thời cả wine32 và wine64 để đảm bảo hỗ trợ toàn diện cho mọi loại ứng dụng Windows.

5. **Cài đặt và xây dựng Payload**:
    - `wine ~/.wine/drive_c/users/kali/AppData/Local/Programs/Python/Python312/python.exe -m pip install --upgrade pip`  
      Nâng cấp pip để đảm bảo phiên bản mới nhất.
    - `wine ~/.wine/drive_c/users/kali/AppData/Local/Programs/Python/Python312/python.exe -m pip install pyinstaller`  
      Cài đặt PyInstaller để đóng gói mã Python thành executable.
    - `wine ~/.wine/drive_c/users/kali/AppData/Local/Programs/Python/Python312/python.exe -m pip install requests cryptography`  
      Cài đặt thư viện requests và cryptography cho chức năng mạng và mã hóa.
    - `wine ~/.wine/drive_c/users/kali/AppData/Local/Programs/Python/Python312/python.exe -m PyInstaller --onefile --noconsole --name "Office365_Setup" auto_demo.py`  
      Sử dụng PyInstaller để tạo file executable đơn giản, không cửa sổ console, đặt tên là "Office365_Setup" từ file auto_demo.py.

### Chi tiết Cách Sử dụng
1. **Khởi động máy ảo**: Khởi động cả Attacker (Kali Linux) và Victim (Windows 10).
2. **Xây dựng Payload trên Attacker**: Thực hiện các lệnh trong bước 5 để tạo file executable "Office365_Setup.exe".
3. **Upload Payload lên Server**: Đưa file "Office365_Setup.exe" lên máy chủ HTTP tại địa chỉ http://192.168.1.9 (sử dụng apache2 để tạo server web).
4. **Victim Tải về và Chạy**: Trên Victim, truy cập http://192.168.1.9 để tải về file "Office365_Setup.exe" và chạy nó.
5. **Quan sát**: Theo dõi quá trình mã hóa file trên Victim và kết nối ngược về Attacker.



