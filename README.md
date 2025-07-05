# 🎮 Caro Deluxe – AI-Powered Strategy Game  
> 🇻🇳 Một trò chơi Caro hiện đại tích hợp trí tuệ nhân tạo mạnh mẽ  
> 🇬🇧 A complete AI-enhanced Gomoku game with polished state management and modular design

---

## 🧠 Overview | Tổng quan

**Caro Deluxe** is a full-featured Gomoku (Caro) game built with Python and Pygame.  
It showcases strong AI capabilities with **Minimax + Alpha-Beta Pruning**, a scalable game architecture using **state machines**, and a variety of player experience features such as match analytics, theme switching, and sound effects.

**Caro Deluxe** là một trò chơi Caro được xây dựng đầy đủ chức năng, tích hợp AI cấp cao, thiết kế mô-đun rõ ràng và nhiều tiện ích tăng trải nghiệm người dùng như phân tích trận đấu, chuyển giao diện, và âm thanh sống động.

---

## 🌟 Features | Tính năng nổi bật

- 🤖 **AI Logic** – Supports multiple difficulty levels from heuristic to *Insane* (Minimax + Alpha-Beta)
- 🧩 **State Machine** – Handles MENU, PLAYING, SETTINGS, GAME OVER, ANALYSIS… like a real game engine
- 💾 **Save & Load** – Persist game progress using JSON files
- 📊 **Match Analysis** – Replay and evaluate gameplay after each round
- 🎵 **Audio & Theme** – Switch between Dark/Light modes, play SFX and music
- 🔧 **Modular Architecture** – Separate modules for rendering, logic, AI, UI, sound, and more

---

## 🛠 Technologies | Công nghệ sử dụng

- **Python 3.x** – Main programming language
- **Pygame** – GUI & game rendering
- **JSON** – Save/Load game data
- **Object-Oriented Design** – Maintainable and scalable code

---

## 🚀 How to Run | Cách chạy game

### Prerequisites / Yêu cầu:
- Python 3.x

### Install Pygame:
```bash
pip install pygame
```
### Start the game:
```bash
python main.py
```
---
### 📁 Folder Structure | Cấu trúc Thư mục
```bash
Caro-Deluxe-1.0/
├── main.py                 # Main entry point
├── config.py               # Game settings
├── levels.py               # AI levels
├── ai_logic.py             # AI algorithms
├── bot.py                  # Bot move logic
├── game_logic.py           # Core game mechanics
├── sound_manager.py        # Sound system
├── utils.py                # Helper functions
├── login_screen.py         # (Optional) login screen
├── renderer.py             # GUI renderer
└── assets/
    ├── fonts/              # Fonts
    ├── images/             # Icons for X/O
    └── sounds/             # SFX: click, win, lose, etc.
```
---
### 📌 Author & Notes
Created by Ngô Nhật Nguyên (nnYunaXYZ) – for learning, portfolio, and MIT-prep projects.
A complete solo-built project done in 7 hours, proving high concentration, algorithmic mastery, and structured thinking.
> 🔗 GitHub: [github.com/NhatNguyenYn](https://github.com/NhatNguyenYn)
---
### 🪪 License
Licensed under the MIT License – Free to use for personal and educational purposes.
