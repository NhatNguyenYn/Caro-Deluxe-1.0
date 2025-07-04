# utils.py
import json
import os

LEADERBOARD_FILE = 'leaderboard.json'
SAVE_GAME_FILE = 'savegame.json'

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_leaderboard(player_name, result):
    data = load_leaderboard()
    if player_name not in data: data[player_name] = {'wins': 0, 'losses': 0, 'draws': 0}
    if result == 'win': data[player_name]['wins'] += 1
    elif result == 'loss': data[player_name]['losses'] += 1
    elif result == 'draw': data[player_name]['draws'] += 1
    save_leaderboard(data)

def save_game_state(game_state_data):
    try:
        with open(SAVE_GAME_FILE, 'w', encoding='utf-8') as f:
            json.dump(game_state_data, f, indent=4, ensure_ascii=False)
        print(f"Đã lưu game vào {SAVE_GAME_FILE}")
        return True
    except Exception as e:
        print(f"Lỗi khi lưu game: {e}")
        return False

def load_game_state():
    if not os.path.exists(SAVE_GAME_FILE):
        print(f"Không tìm thấy file lưu game: {SAVE_GAME_FILE}")
        return None
    try:
        with open(SAVE_GAME_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Đã tải game từ {SAVE_GAME_FILE}")
        return data
    except Exception as e:
        print(f"Lỗi khi tải game: {e}")
        return None

def delete_save_game():
    if os.path.exists(SAVE_GAME_FILE):
        os.remove(SAVE_GAME_FILE)
        print(f"Đã xóa file lưu game: {SAVE_GAME_FILE}")