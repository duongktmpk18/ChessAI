# Chess AI ♟️

Một tựa game Cờ vua mã nguồn mở được phát triển bằng Python và thư viện Pygame. Dự án cung cấp một giao diện tương tác trực quan, đẹp mắt kết hợp cùng với engine AI tích hợp sẵn, cho phép bạn thi đấu với máy hoặc giải trí với bạn bè.

## ✨ Tính năng nổi bật

- **Chế độ chơi đa dạng:** 
  - **Player vs Player**: Đấu 2 người trực tiếp trên cùng một màn hình.
  - **Player vs AI**: Thử thách bản thân với Engine máy tính được tối ưu thông qua thuật toán Minimax và Sunfish.
- **Hệ thống Đồng hồ thi đấu (Time Controls):** Tích hợp tính năng đồng hồ đếm ngược với đa dạng các thể thức cờ chuyên nghiệp: 
  - Bullet (1 phút)
  - Blitz (3 phút + 2s cộng thêm)
  - Rapid (10 phút)
  - Classical (30 phút)
  - Unlimited (Không tính thời gian - dùng cho tập luyện)
- **Đồ họa & Âm thanh sống động:** 
  - Hình nền không gian 3D Pixel Art động.
  - Hiệu ứng phát sáng và âm thanh sống động (click, hover) khi tương tác với UI và di chuyển quân.
- **Tính năng mở rộng:** Menu Cài đặt nhanh trong trận đấu giúp bạn có thể Đầu hàng, Reset lại ván mới hoặc thoát ra màn hình chính bất kỳ lúc nào.

## 🚀 Hướng dẫn Cài đặt & Khởi chạy

### Yêu cầu hệ thống
- **Python** (phiên bản 3.8 trở lên)
- **Pygame** (khuyên dùng phiên bản 2.6.x)

### 1. Tải mã nguồn (Clone repository)
Mở Terminal / Command Prompt và chạy lệnh sau để tải toàn bộ mã nguồn về máy:
```bash
git clone https://github.com/duongktmpk18/ChessAI.git
cd ChessAI
```

### 2. Thiết lập Môi trường ảo (Tùy chọn nhưng khuyến nghị)
Bạn nên tạo một môi trường ảo để chứa các thư viện độc lập cho dự án:
- **Trên Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **Trên macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Cài đặt các thư viện cần thiết
Sử dụng `pip` để tải `pygame`:
```bash
pip install pygame
```

### 4. Khởi chạy Trò chơi
Sau khi cài đặt xong, bạn gõ lệnh dưới đây để bật game:
```bash
python main.py
```

## 🎮 Cách điều khiển
- **Menu:** Dùng **Chuột trái** để chọn các nút tùy chỉnh trên màn hình.
- **Di chuyển quân:** 
  1. Click chuột trái vào quân cờ bạn muốn đi (các ô có thể đi hợp lệ sẽ tự động được làm nổi bật).
  2. Click chuột trái lần nữa vào vị trí đích đến để di chuyển.
- **Luật Hết giờ (Flagging):** Nếu bạn chơi ở chế độ có tính giờ, bên nào để đồng hồ chạy về mức `0:00` trước sẽ ngay lập tức bị xử thua (Won on Time).

## 🛠 Cấu trúc mã nguồn chính
- `main.py`: Điều khiển vòng lặp chính của trò chơi (Game Loop), vẽ giao diện UI và quản lý thời gian.
- `pieces.py`: Nơi định nghĩa các luật đi hợp lệ cho từng loại quân cờ.
- `tools.py`: Các hàm tiện ích hỗ trợ logic và toán học của bàn cờ.
- `AI.py` / `AI_sunfish.py`: Xử lý thuật toán trí tuệ nhân tạo.

---
*Chúc bạn có những giờ phút căng não và thú vị cùng Chess AI!*
