# config.py

import pygame

# --- KÍCH THƯỚC & CÀI ĐẶT MẶC ĐỊNH ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
DEFAULT_BOARD_ROWS = 10
DEFAULT_BOARD_COLS = 10
DEFAULT_WIN_CONDITION = 5

# --- MÀU SẮC (RGB) ---
# Các biến này sẽ được cập nhật khi theme thay đổi
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
BUTTON_HOVER_COLOR = (43, 185, 175)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (234, 234, 234)
X_COLOR = (239, 231, 210)
O_COLOR = (84, 84, 84)
WINNING_LINE_COLOR = (255, 215, 0)
INPUT_BOX_ACTIVE_COLOR = (200, 200, 200)
INPUT_BOX_INACTIVE_COLOR = (100, 100, 100)
LAST_MOVE_HIGHLIGHT_COLOR = (255, 255, 0, 80)

# --- ĐỊNH NGHĨA CÁC THEME KHÁC NHAU ---
THEMES = {
    "light": {
        "BG_COLOR": (28, 170, 156), "LINE_COLOR": (23, 145, 135),
        "BUTTON_HOVER_COLOR": (43, 185, 175), "TEXT_COLOR": (50, 50, 50),
        "WHITE": (255, 255, 255), "BLACK": (0, 0, 0),
        "X_COLOR": (239, 231, 210), "O_COLOR": (84, 84, 84),
        "WINNING_LINE_COLOR": (255, 215, 0), "LAST_MOVE_HIGHLIGHT_COLOR": (255, 255, 0, 80)
    },
    "dark": {
        "BG_COLOR": (30, 30, 30), "LINE_COLOR": (60, 60, 60),
        "BUTTON_HOVER_COLOR": (90, 90, 90), "TEXT_COLOR": (230, 230, 230),
        "WHITE": (255, 255, 255), "BLACK": (0, 0, 0),
        "X_COLOR": (200, 200, 200), "O_COLOR": (50, 50, 50),
        "WINNING_LINE_COLOR": (255, 0, 0), "LAST_MOVE_HIGHLIGHT_COLOR": (0, 255, 255, 80)
    }
}

# --- FONT CHỮ ---
pygame.font.init()
FONT_PATH = 'assets/fonts/Roboto-SemiBold.ttf'
# FONT_PATH = None

# --- CÀI ĐẶT ÂM THANH MẶC ĐỊNH ---
DEFAULT_VOLUME_MUSIC = 0.5
DEFAULT_VOLUME_SFX = 0.8