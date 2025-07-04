# levels.py

LEVELS = [
    {
        "name": "Màn 1: 3x3",
        "rows": 3, "cols": 3, "win_condition": 3,
        "difficulty": "easy", "description": "Làm quen với luật chơi cơ bản."
    },
    {
        "name": "Màn 2: 5x5",
        "rows": 5, "cols": 5, "win_condition": 4,
        "difficulty": "medium", "description": "Bot sẽ biết cách chặn bạn."
    },
    {
        "name": "Màn 3: 10x10",
        "rows": 10, "cols": 10, "win_condition": 5,
        "difficulty": "hard", "description": "Thử thách thực sự bắt đầu."
    },
    {
        "name": "Màn 4: 15x15",
        "rows": 15, "cols": 15, "win_condition": 5,
        "difficulty": "hard", "description": "Liệu bạn có thể chiến thắng?"
    },
    {
        "name": "Màn 5: Insane",
        "rows": 3, "cols": 3, "win_condition": 3,
        "difficulty": "insane", # Sử dụng AI Minimax
        "description": "Bot sẽ không bao giờ thua. Bạn chỉ có thể hòa hoặc thua."
    }
]