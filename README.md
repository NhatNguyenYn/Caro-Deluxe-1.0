# 🎮 Caro Deluxe – AI-Powered Strategy Game  
# 🎮 Caro Deluxe – Trò chơi chiến thuật tích hợp trí tuệ nhân tạo

> A complete and well-structured implementation of the classic Caro (Gomoku) game using Python and Pygame, featuring a powerful AI system and professional state management.  
> Một phiên bản Caro hoàn chỉnh và có cấu trúc rõ ràng, được phát triển bằng Python và Pygame, tích hợp hệ thống AI mạnh mẽ cùng quản lý trạng thái chuyên nghiệp.

---

## 🧠 Features / Tính năng nổi bật

- 🎨 **Modular Architecture**: Code organized into clear modules – rendering, game logic, AI, utilities...  
  Cấu trúc module hóa rõ ràng giữa giao diện, logic game, AI và tiện ích.

- 🧩 **State Machine**: Manage game screens (MENU, PLAYING, PAUSED, SETTINGS, GAME_OVER, ANALYSIS...)  
  Sử dụng máy trạng thái để kiểm soát các màn hình game.

- 🤖 **AI with Minimax + Alpha-Beta Pruning**: From basic heuristic levels to "Insane" mode  
  Trí tuệ nhân tạo từ heuristic đơn giản đến nâng cao (Minimax + cắt tỉa Alpha-Beta).

- 📊 **Match Analysis**: Replay & analyze moves after each game  
  Phân tích lại ván chơi giúp người dùng hiểu chiến thuật.

- 💾 **Save/Load System**: Support saving games via JSON  
  Lưu và tải game bằng định dạng JSON.

- 🎵 **Audio & Theme**: Dark/light mode, sound effects, background music  
  Giao diện tối/sáng, hiệu ứng âm thanh, nhạc nền sinh động.

---

## 🚀 How to Run / Cách chạy

1. **Install Python 3.x**  
   Cài đặt Python 3.x từ [python.org](https://www.python.org/)

2. **Install dependencies** / Cài thư viện: pip install pygame
3. **Run the game / Chạy game: python main.py

---

## 📁 Project Folder Structure / Cấu trúc Thư mục Dự án "Caro Deluxe"
```bash
Caro-Deluxe-1.0/
├── main.py               # Điểm khởi động chính của game
├── config.py             # Thiết lập cấu hình (màu sắc, âm thanh, độ khó)
├── levels.py             # Cài đặt các cấp độ AI
├── ai_logic.py           # Thuật toán AI (Heuristic + Minimax)
├── bot.py                # Quản lý các lượt đi của bot
├── game_logic.py         # Logic xử lý ván cờ
├── sound_manager.py      # Hệ thống âm thanh
├── utils.py              # Hàm tiện ích phụ trợ
├── login_screen.py       # Màn hình đăng nhập (nếu có)
├── renderer.py           # Giao diện hiển thị (Tkinter/Pygame)
└── assets/               # Thư mục tài nguyên
    ├── fonts/
    │   └── Roboto-SemiBold.ttf   # Font chữ sử dụng
    ├── images/
    │   ├── x.png                 # Ảnh quân X (optional)
    │   └── o.png                 # Ảnh quân O (optional)
    └── sounds/
        ├── click.mp3            # Âm thanh khi click nút
        ├── place.mp3            # Âm thanh khi đặt quân cờ
        ├── win.mp3              # Âm thanh khi thắng
        ├── lose.mp3             # Âm thanh khi thua/hòa
        └── music.mp3            # Nhạc nền trong game
```
---
## 📝 License / Giấy phép
This project is licensed under the MIT License.
Dự án được phát hành theo giấy phép MIT – tự do sử dụng với mục đích học tập và cá nhân.
© 2025 by nnYunaXYZ – All rights reserved.

---
Author: nnYunaXYZ
