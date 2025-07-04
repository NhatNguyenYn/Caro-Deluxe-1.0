# login_screen.py
import pygame
import sys
import os
import json
import config # Import config để truy cập các hằng số

# Hàm tiện ích vẽ text và button
def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y)) if center else text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, rect, text, font, mouse_pos):
    btn_color = config.BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else config.LINE_COLOR
    pygame.draw.rect(surface, btn_color, rect, border_radius=15)
    draw_text(surface, text, font, config.WHITE, rect.centerx, rect.centery, center=True)


def get_username_input(screen, font_title, font_menu, font_status, sound_manager, clock):
    """
    Hiển thị màn hình nhập tên người dùng hoặc chọn chơi ẩn danh.
    Trả về tên người dùng đã chọn.
    """
    username = ""
    input_box = pygame.Rect(100, config.SCREEN_HEIGHT // 2 - 25, 400, 50)
    input_box_active = True
    
    anonymous_button = pygame.Rect(150, input_box.bottom + 80, 300, 60)
    
    anonymous_player_count = 0
    if os.path.exists('leaderboard.json'):
        try:
            with open('leaderboard.json', 'r', encoding='utf-8') as f:
                leaderboard_data = json.load(f)
            for name in leaderboard_data.keys():
                if name.startswith("Player "):
                    try:
                        num = int(name.split(" ")[1])
                        if num > anonymous_player_count:
                            anonymous_player_count = num
                    except ValueError:
                        pass
        except (IOError, json.JSONDecodeError):
            print("Cảnh báo: Không thể đọc file leaderboard.json để tạo tên ẩn danh. Bắt đầu từ Player 1.")
            pass


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_box_active = True
                else:
                    input_box_active = False
                
                if anonymous_button.collidepoint(mouse_pos):
                    sound_manager.play('click')
                    anonymous_player_count += 1
                    return f"Player {anonymous_player_count}"

            if event.type == pygame.KEYDOWN and input_box_active:
                if event.key == pygame.K_RETURN:
                    if username:
                        sound_manager.play('click')
                        return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode
        
        screen.fill(config.BG_COLOR)
        draw_text(screen, "Nhập tên của bạn", font_title, config.WHITE, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3, center=True)
        
        box_color = config.INPUT_BOX_ACTIVE_COLOR if input_box_active else config.INPUT_BOX_INACTIVE_COLOR
        pygame.draw.rect(screen, box_color, input_box, 2)
        
        text_surface = font_menu.render(username, True, config.TEXT_COLOR)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        
        draw_text(screen, "Hoặc nhấn ENTER để tiếp tục", font_status, config.TEXT_COLOR, config.SCREEN_WIDTH // 2, input_box.bottom + 40, center=True)

        draw_button(screen, anonymous_button, "Chơi ẩn danh", font_menu, mouse_pos)

        pygame.display.update()
        clock.tick(60)

    return "Guest"