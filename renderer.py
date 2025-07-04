# renderer.py
import pygame
import config
import random
import math
from levels import LEVELS
from utils import load_leaderboard

# --- CÁC HÀM VẼ TIỆN ÍCH ---
def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color); text_rect = text_obj.get_rect(center=(x, y)) if center else text_obj.get_rect(topleft=(x, y)); surface.blit(text_obj, text_rect)
def draw_button(surface, rect, text, font, mouse_pos):
    btn_color = config.BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else config.LINE_COLOR; pygame.draw.rect(surface, btn_color, rect, border_radius=15); draw_text(surface, text, font, config.WHITE, rect.centerx, rect.centery, center=True)
def draw_slider(surface, rect, value):
    pygame.draw.rect(surface, (200, 200, 200), rect, border_radius=5)
    fill_rect = pygame.Rect(rect.left, rect.top, int(value * rect.width), rect.height)
    pygame.draw.rect(surface, config.LINE_COLOR, fill_rect, border_radius=5)
    handle_x = rect.x + int(value * rect.width)
    pygame.draw.circle(surface, config.WHITE, (handle_x, rect.centery), 12)

def draw_text_wrapped(surface, text, font, color, rect, align_center=True):
    words = [word.split(' ') for word in text.splitlines()]
    lines = []
    current_line = []
    current_line_width = 0
    space_width = font.size(' ')[0]

    for word in words[0]:
        word_width, word_height = font.size(word)
        if current_line_width + word_width + space_width > rect.width and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_line_width = word_width
        else:
            current_line.append(word)
            current_line_width += word_width + space_width
    if current_line: lines.append(' '.join(current_line))

    total_text_height = len(lines) * font.get_height()
    start_y = rect.centery - total_text_height // 2

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect()
        line_rect.top = start_y + i * font.get_height()
        
        if align_center: line_rect.centerx = rect.centerx
        else: line_rect.left = rect.left
        surface.blit(line_surface, line_rect)

def shake_screen(game_obj):
    if not hasattr(game_obj, 'shake_timer') or game_obj.shake_timer <= 0: return (0, 0)
    game_obj.shake_timer -= 1 / game_obj.clock.get_fps()
    if game_obj.shake_timer <= 0: return (0, 0)
    intensity = 5 * game_obj.shake_timer / 0.5
    offset_x = random.uniform(-intensity, intensity)
    offset_y = random.uniform(-intensity, intensity)
    return (offset_x, offset_y)

def draw_notification(surface, game_obj):
    if not hasattr(game_obj, 'notification') or not game_obj.notification: return
    message, timer = game_obj.notification
    if timer <= 0: game_obj.notification = None; return
    text_surface_noti = game_obj.font_menu.render(message, True, config.WHITE); text_width_noti, text_height_noti = text_surface_noti.get_size()
    popup_padding_x = 40; popup_padding_y = 20; popup_width = text_width_noti + popup_padding_x; popup_height = text_height_noti + popup_padding_y
    notification_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA); notification_surface.fill((0, 0, 0, 180))
    pygame.draw.rect(notification_surface, config.WHITE, (0, 0, popup_width, popup_height), 2, border_radius=10)
    draw_text(notification_surface, message, game_obj.font_menu, config.WHITE, popup_width // 2, popup_height // 2, center=True)
    surface.blit(notification_surface, (config.SCREEN_WIDTH // 2 - popup_width // 2, config.SCREEN_HEIGHT // 2 - popup_height // 2))

# === HÀM VẼ CÁC THÀNH PHẦN BÀN CỜ (LỚP ĐẦU TIÊN) ===
def draw_game_board_elements(surface, game_obj):
    rows_to_display, cols_to_display = game_obj.board_rows, game_obj.board_cols
    square_size, line_width = game_obj.square_size, game_obj.line_width
    is_analysis_screen = game_obj.game_state == 'ANALYSIS'
    if is_analysis_screen and game_obj.analysis_results:
        current_analysis = game_obj.analysis_results[game_obj.current_analysis_turn_index]
        rows_to_display = current_analysis['rows']; cols_to_display = current_analysis['cols']
        square_size = config.SCREEN_WIDTH // cols_to_display
        if cols_to_display == 3: square_size = config.SCREEN_WIDTH // 3
        elif cols_to_display == 5: square_size = config.SCREEN_WIDTH // 5
        line_width = max(1, int(square_size * 0.1))
        board_to_draw = current_analysis['board_before_move']
    else: board_to_draw = game_obj.board
    for r in range(1, rows_to_display): pygame.draw.line(surface, config.LINE_COLOR, (0, r * square_size), (config.SCREEN_WIDTH, r * square_size), line_width)
    for c in range(1, cols_to_display): pygame.draw.line(surface, config.LINE_COLOR, (c * square_size, 0), (c * square_size, rows_to_display * square_size), line_width)
    if not is_analysis_screen and game_obj.last_move:
        r, c = game_obj.last_move; s = pygame.Surface((square_size, square_size), pygame.SRCALPHA); s.fill(config.LAST_MOVE_HIGHLIGHT_COLOR); surface.blit(s, (c * square_size, r * square_size))
    for row in range(rows_to_display):
        for col in range(cols_to_display):
            piece_char = board_to_draw[row][col]
            if piece_char == 'X':
                if game_obj.x_img: img_margin = int(square_size * 0.1); surface.blit(game_obj.x_img, (col * square_size + img_margin, row * square_size + img_margin))
                else: margin = int(square_size * 0.2); thickness = max(2, int(square_size * 0.1)); pygame.draw.line(surface, config.X_COLOR, (col*square_size+margin, row*square_size+margin), (col*square_size+square_size-margin, row*square_size+square_size-margin), thickness); pygame.draw.line(surface, config.X_COLOR, (col*square_size+margin, row*square_size+square_size-margin), (col*square_size+square_size-margin, row*square_size+margin), thickness)
            elif piece_char == 'O':
                if game_obj.o_img: img_margin = int(square_size * 0.1); surface.blit(game_obj.o_img, (col * square_size + img_margin, row * square_size + img_margin))
                else: center = (col*square_size+square_size//2, row*square_size+square_size//2); radius = int(square_size/2*0.7); thickness = max(2, int(square_size*0.1)); pygame.draw.circle(surface, config.O_COLOR, center, radius, thickness)
    if is_analysis_screen:
        player_move_r, player_move_c = current_analysis['player_actual_move']; best_move_r, best_move_c = current_analysis['best_move_suggested']
        highlight_player_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA); highlight_player_surface.fill((255, 0, 0, 100)); surface.blit(highlight_player_surface, (player_move_c * square_size, player_move_r * square_size))
        highlight_best_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA); highlight_best_surface.fill((0, 255, 0, 100)); surface.blit(highlight_best_surface, (best_move_c * square_size, best_move_r * square_size))

def draw_winning_line_animation(surface, game_obj):
    # Dòng if đầu tiên nên được tách riêng để đảm bảo nó luôn kiểm tra đúng
    if not game_obj.winning_line_data:
        return
        
    # Bây giờ, chúng ta biết chắc chắn game_obj.winning_line_data có giá trị
    # nên có thể giải nén nó một cách an toàn.
    coords, player, progress = game_obj.winning_line_data

    # Các dòng còn lại giữ nguyên
    if len(coords) < 2: return
    start_point_x, start_point_y = coords[0][1] * game_obj.square_size + game_obj.square_size // 2, coords[0][0] * game_obj.square_size + game_obj.square_size // 2
    end_point_x, end_point_y = coords[-1][1] * game_obj.square_size + game_obj.square_size // 2, coords[-1][0] * game_obj.square_size + game_obj.square_size // 2
    current_x = start_point_x + (end_point_x - start_point_x) * progress; current_y = start_point_y + (end_point_y - start_point_y) * progress
    line_thickness = max(5, int(game_obj.square_size * 0.1)); pygame.draw.line(surface, config.WINNING_LINE_COLOR, (start_point_x, start_point_y), (current_x, current_y), line_thickness)


# --- CÁC HÀM VẼ UI CHI TIẾT (sẽ được gọi từ draw_ui_layer) ---
def draw_menu_ui(surface, game_obj, mouse_pos):
    draw_text(surface, 'Caro Deluxe', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, 50, center=True)
    draw_button(surface, game_obj.pvp_button, 'Chơi 2 người', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.campaign_button, 'Người vs Máy', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.leaderboard_button, 'Bảng Xếp Hạng', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.settings_button, 'Cài Đặt', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.about_button, 'Thông Tin', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.load_game_button, 'Tải Game', game_obj.font_menu, mouse_pos)
    draw_notification(surface, game_obj)

def draw_campaign_ui(surface, game_obj, mouse_pos):
    draw_text(surface, 'Chọn Màn Chơi', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, 50, center=True)
    y_pos = 150
    game_obj.level_buttons = []
    
    # Vòng lặp vẽ các nút chọn màn chơi (giữ nguyên)
    for level in LEVELS: 
        button_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 160, y_pos, 320, 70)
        game_obj.level_buttons.append(button_rect)
        draw_button(surface, button_rect, level["name"], game_obj.font_menu, mouse_pos)
        y_pos += 90

    # === SỬA ĐỔI TẠI ĐÂY: Đặt lại vị trí cho nút "Menu" ===
    # Đặt nút về góc dưới cùng bên phải màn hình
    button_width = 200
    button_height = 60
    button_padding = 20
    game_obj.back_to_menu_button.size = (button_width, button_height)
    game_obj.back_to_menu_button.topleft = (
        config.SCREEN_WIDTH - button_width - button_padding, 
        config.SCREEN_HEIGHT - button_height - button_padding
    )
    # Sau khi đặt đúng vị trí, mới tiến hành vẽ
    draw_button(surface, game_obj.back_to_menu_button, 'Menu', game_obj.font_menu, mouse_pos)
    # ========================================================
    
    draw_notification(surface, game_obj)

def draw_playing_ui(surface, game_obj): # Hàm này được gọi khi game đang chơi
    if not game_obj.game_over:
        draw_text(surface, f"Lượt của: {game_obj.current_player}", game_obj.font_status, config.WHITE, 20, game_obj.board_rows * game_obj.square_size + 20)
    draw_notification(surface, game_obj) # Đặt notification ở đây


def draw_game_over_ui(surface, game_obj, mouse_pos):
    message = f"{game_obj.winner} thắng!" if game_obj.winner else "Hòa!"
    draw_text(surface, message, game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 100, center=True)
    
    button_width = 200; button_height = 60; button_spacing = 20
    analyze_button_x = config.SCREEN_WIDTH // 2 - 150
    game_obj.analyze_button.topleft = (analyze_button_x, config.SCREEN_HEIGHT // 2 + 50)
    game_obj.analyze_button.size = (300, 60) # Đảm bảo kích thước đúng
    draw_button(surface, game_obj.analyze_button, 'Phân tích trận', game_obj.font_menu, mouse_pos)
    
    play_again_width = 220; menu_width = 200; total_width = play_again_width + menu_width + button_spacing
    play_again_x = config.SCREEN_WIDTH // 2 - total_width // 2
    menu_x = play_again_x + play_again_width + button_spacing
    game_obj.play_again_button.topleft = (play_again_x, config.SCREEN_HEIGHT // 2 + 120)
    game_obj.back_to_menu_button.topleft = (menu_x, config.SCREEN_HEIGHT // 2 + 120)
    draw_button(surface, game_obj.play_again_button, 'Chơi lại', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.back_to_menu_button, 'Menu', game_obj.font_menu, mouse_pos)
    
    draw_notification(surface, game_obj)

def draw_leaderboard_ui(surface, game_obj, mouse_pos):
    from utils import load_leaderboard
    surface.fill(config.BG_COLOR)
    draw_text(surface, 'Bảng Xếp Hạng', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, 50, center=True)
    leaderboard = load_leaderboard()
    sorted_players = sorted(leaderboard.items(), key=lambda item: (item[1]['wins'], -item[1]['losses']), reverse=True)
    
    y_pos_header = 150
    y_pos_start_data = y_pos_header + 50

    # Vị trí các cột đã được căn chỉnh lại để có khoảng trống
    x_rank_col = 25
    x_name_col = 150
    x_wins_col = 340
    x_losses_col = 440
    x_draws_col = 530 # Tăng nhẹ khoảng cách
    
    # === SỬA ĐỔI 1: VẼ CÁC TIÊU ĐỀ CỘT RIÊNG BIỆT ===
    # Lỗi chính trong hình ảnh của bạn là các tiêu đề được vẽ chung một chuỗi.
    # Bây giờ chúng ta sẽ vẽ từng cái một tại vị trí đã định.
    header_font = game_obj.font_status
    draw_text(surface, "Hạng", header_font, config.WHITE, x_rank_col, y_pos_header, center=False)
    draw_text(surface, "Tên", header_font, config.WHITE, x_name_col, y_pos_header, center=False)
    draw_text(surface, "Thắng", header_font, config.WHITE, x_wins_col, y_pos_header, center=False)
    draw_text(surface, "Thua", header_font, config.WHITE, x_losses_col, y_pos_header, center=False)
    draw_text(surface, "Hòa", header_font, config.WHITE, x_draws_col, y_pos_header, center=False)
    # ================================================

    y_pos = y_pos_start_data
    data_font = game_obj.font_status

    for i, (name, stats) in enumerate(sorted_players[:10]):
        # === SỬA ĐỔI 2: LOẠI BỎ MÀU XEN KẼ ===
        # Sử dụng một màu duy nhất cho tất cả các dòng dữ liệu.
        row_color = config.TEXT_COLOR 
        # ========================================

        draw_text(surface, f"#{i+1}", data_font, row_color, x_rank_col, y_pos, center=False)
        
        display_name = (name[:15] + '...') if len(name) > 15 else name 
        draw_text(surface, display_name, data_font, row_color, x_name_col, y_pos, center=False)
        
        # Căn phải các số liệu vẫn giữ nguyên để đảm bảo cột thẳng hàng
        wins_text = str(stats["wins"])
        wins_rect = data_font.render(wins_text, True, row_color).get_rect(topright=(x_wins_col + 50, y_pos))
        surface.blit(data_font.render(wins_text, True, row_color), wins_rect)

        losses_text = str(stats["losses"])
        losses_rect = data_font.render(losses_text, True, row_color).get_rect(topright=(x_losses_col + 50, y_pos))
        surface.blit(data_font.render(losses_text, True, row_color), losses_rect)

        draws_text = str(stats["draws"])
        draws_rect = data_font.render(draws_text, True, row_color).get_rect(topright=(x_draws_col + 50, y_pos))
        surface.blit(data_font.render(draws_text, True, row_color), draws_rect)

        y_pos += 40
    
    # Đặt nút quay lại ở giữa, phía dưới
    button_rect = pygame.Rect(config.SCREEN_WIDTH / 2 - 100, config.SCREEN_HEIGHT - 80, 200, 60)
    game_obj.back_to_menu_button.size = button_rect.size
    game_obj.back_to_menu_button.center = button_rect.center
    draw_button(surface, game_obj.back_to_menu_button, 'Quay lại', game_obj.font_menu, mouse_pos)
    
    draw_notification(surface, game_obj)

def draw_settings_ui(surface, game_obj, mouse_pos):
    surface.fill(config.BG_COLOR)
    draw_text(surface, 'Cài Đặt', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, 50, center=True)
    
    # Kích thước và khoảng cách chung cho các thành phần UI
    text_x_start = 100 # Vị trí X bắt đầu cho các dòng text mô tả
    slider_width = 300
    slider_height = 15
    button_small_width = 120
    button_small_height = 50
    block_padding_y = 70 # Tăng khoảng cách giữa các khối một chút

    # 1. PHẦN NHẠC NỀN
    y_current = 150 
    
    music_text_surface = game_obj.font_menu.render("Nhạc Nền:", True, config.WHITE)
    surface.blit(music_text_surface, (text_x_start, y_current))
    
    music_text_rect = music_text_surface.get_rect(topleft=(text_x_start, y_current))
    game_obj.music_toggle_button.topleft = (music_text_rect.right + 20, y_current - 5)
    game_obj.music_toggle_button.size = (button_small_width, button_small_height)
    draw_button(surface, game_obj.music_toggle_button, "BẬT" if pygame.mixer.music.get_busy() else "TẮT", game_obj.font_menu, mouse_pos)
    
    y_current = music_text_rect.bottom + 20
    music_volume_text_surface = game_obj.font_menu.render("Âm lượng nhạc:", True, config.WHITE)
    surface.blit(music_volume_text_surface, (text_x_start, y_current))
    
    game_obj.music_volume_slider_rect.topleft = (text_x_start, y_current + music_volume_text_surface.get_height() + 10)
    game_obj.music_volume_slider_rect.size = (slider_width, slider_height)
    draw_slider(surface, game_obj.music_volume_slider_rect, game_obj.sound_manager.volume_music)
    
    # === SỬA ĐỔI 1: Tăng khoảng cách cho số phần trăm ===
    percent_text_x = game_obj.music_volume_slider_rect.right + 50 # Tăng từ 20 -> 40
    draw_text(surface, f"{int(game_obj.sound_manager.volume_music * 100)}%", game_obj.font_menu, config.WHITE, percent_text_x, game_obj.music_volume_slider_rect.centery, center=True)
    # ==================================================

    
    # 2. PHẦN HIỆU ỨNG ÂM THANH
    y_current = game_obj.music_volume_slider_rect.bottom + block_padding_y
    
    sfx_text_surface = game_obj.font_menu.render("Âm lượng SFX:", True, config.WHITE)
    surface.blit(sfx_text_surface, (text_x_start, y_current))
    
    game_obj.sfx_volume_slider_rect.topleft = (text_x_start, y_current + sfx_text_surface.get_height() + 10)
    game_obj.sfx_volume_slider_rect.size = (slider_width, slider_height)
    draw_slider(surface, game_obj.sfx_volume_slider_rect, game_obj.sound_manager.volume_sfx)

    # === SỬA ĐỔI 2: Tăng khoảng cách cho số phần trăm ===
    percent_text_x_sfx = game_obj.sfx_volume_slider_rect.right + 50 # Tăng từ 20 -> 40
    draw_text(surface, f"{int(game_obj.sound_manager.volume_sfx * 100)}%", game_obj.font_menu, config.WHITE, percent_text_x_sfx, game_obj.sfx_volume_slider_rect.centery, center=True)
    # ==================================================
    
    # 3. PHẦN CHẾ ĐỘ NỀN (THEME)
    y_current = game_obj.sfx_volume_slider_rect.bottom + block_padding_y 
    
    theme_text_surface = game_obj.font_menu.render("Chế độ nền:", True, config.WHITE)
    surface.blit(theme_text_surface, (text_x_start, y_current))
    
    # === SỬA ĐỔI 3: Sửa lại cách tính vị trí nút Theme ===
    theme_text_rect = theme_text_surface.get_rect(topleft=(text_x_start, y_current))
    theme_toggle_button_x = theme_text_rect.right + 20 # Đặt nút ngay sau text, tương tự nút BẬT/TẮT
    game_obj.theme_toggle_button.topleft = (theme_toggle_button_x, y_current - 5)
    game_obj.theme_toggle_button.size = (button_small_width, button_small_height)
    draw_button(surface, game_obj.theme_toggle_button, game_obj.current_theme_name.upper(), game_obj.font_menu, mouse_pos)
    # ==================================================
    
    # Nút quay lại (đặt ở dưới cùng)
    game_obj.back_to_menu_button.topleft = (config.SCREEN_WIDTH - 20 - 200, config.SCREEN_HEIGHT - 20 - 60)
    draw_button(surface, game_obj.back_to_menu_button, 'Quay lại', game_obj.font_menu, mouse_pos)
    
    draw_notification(surface, game_obj)

def draw_about_ui(surface, game_obj, mouse_pos):
    surface.fill(config.BG_COLOR)
    draw_text(surface, 'Credits', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, 50, center=True)
    about_text_lines = [
        "Phiên bản: Caro Deluxe 1.0",
        "Phát triển bởi: nnYunaXYZ",
        "",
        "Đây là một dự án nhỏ, tâm huyết của mình","Hoàn thành chính thức trong ~7 giờ",""
        "", "Đồ họa & Âm thanh: Nguồn mở / Winsound",
        "AI Bot: Minimax với Alpha-Beta Pruning", "", "Cảm ơn bạn đã trải nghiệm!"
    ]
    y_pos = 150
    for line in about_text_lines:
        draw_text(surface, line, game_obj.font_status, config.TEXT_COLOR, config.SCREEN_WIDTH // 2, y_pos, center=True)
        y_pos += 30
    button_width = 200
    button_height = 60
    game_obj.back_to_menu_button.topleft = (config.SCREEN_WIDTH - 20 - button_width, config.SCREEN_HEIGHT - 20 - button_height)
    draw_button(surface, game_obj.back_to_menu_button, 'Quay lại', game_obj.font_menu, mouse_pos)
    draw_notification(surface, game_obj)

def draw_pause_ui(surface, game_obj, mouse_pos):
    draw_text(surface, 'PAUSED', game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 150, center=True)
    button_height_standard = 60
    button_spacing = 20
    num_buttons_in_pause_menu = 4
    total_buttons_height = num_buttons_in_pause_menu * button_height_standard + (num_buttons_in_pause_menu - 1) * button_spacing
    start_y_for_buttons = config.SCREEN_HEIGHT // 2 - total_buttons_height // 2 + 30
    game_obj.resume_button.topleft = (config.SCREEN_WIDTH // 2 - game_obj.resume_button.width // 2, start_y_for_buttons)
    game_obj.main_menu_button.topleft = (config.SCREEN_WIDTH // 2 - game_obj.main_menu_button.width // 2, start_y_for_buttons + game_obj.resume_button.height + button_spacing)
    game_obj.save_game_button.topleft = (config.SCREEN_WIDTH // 2 - game_obj.save_game_button.width // 2, start_y_for_buttons + 2 * (game_obj.resume_button.height + button_spacing))
    game_obj.quit_game_button.topleft = (config.SCREEN_WIDTH // 2 - game_obj.quit_game_button.width // 2, start_y_for_buttons + 3 * (game_obj.resume_button.height + button_spacing))
    game_obj.pause_buttons = {
        'resume': game_obj.resume_button,
        'main_menu': game_obj.main_menu_button,
        'save': game_obj.save_game_button,
        'quit': game_obj.quit_game_button
    }
    draw_button(surface, game_obj.pause_buttons['resume'], 'Tiếp tục', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.pause_buttons['main_menu'], 'Menu chính', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.pause_buttons['save'], 'Lưu game', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.pause_buttons['quit'], 'Thoát game', game_obj.font_menu, mouse_pos)
    button_width = 200
    button_height = 60
    game_obj.back_to_menu_button.topleft = (config.SCREEN_WIDTH - 20 - button_width, config.SCREEN_HEIGHT - 20 - button_height)
    draw_button(surface, game_obj.back_to_menu_button, 'Menu', game_obj.font_menu, mouse_pos)
    draw_notification(surface, game_obj)

def draw_analysis_ui(surface, game_obj, mouse_pos):
    current_analysis = game_obj.analysis_results[game_obj.current_analysis_turn_index]

    #text_info_y_start = 80
    #draw_text(surface, f"Lượt: {current_analysis['turn']} (Bạn đi)", game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, text_info_y_start, center=True)
    #player_move_rect = pygame.Rect(50, text_info_y_start + 70, config.SCREEN_WIDTH - 100, 50)
    #draw_text_wrapped(surface, f"Nước đi của bạn: {current_analysis['player_actual_move']}", game_obj.font_menu, config.TEXT_COLOR, player_move_rect)
    #best_move_text = f"Nước tốt nhất: {current_analysis['best_move_suggested']}"
    #best_move_rect_container = pygame.Rect(50, text_info_y_start + 120, config.SCREEN_WIDTH - 100, 70)
    #if current_analysis['is_missed_win']:
        #draw_text_wrapped(surface, best_move_text + " (BỎ LỠ CƠ HỘI THẮNG!)", game_obj.font_menu, (255, 0, 0), best_move_rect_container)
    #else:
        #draw_text_wrapped(surface, best_move_text, game_obj.font_menu, config.TEXT_COLOR, best_move_rect_container)
    
    
    button_width = 100
    button_height = 60
    button_spacing = 20
    y_buttons_row = config.SCREEN_HEIGHT - 150
    game_obj.back_to_menu_button.topright = (config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 80)
    turn_text_surface = game_obj.font_menu.render(f"{game_obj.current_analysis_turn_index + 1}/{len(game_obj.analysis_results)}", True, config.WHITE)
    turn_text_width = turn_text_surface.get_width()
    prev_x = config.SCREEN_WIDTH // 2 - turn_text_width / 2 - button_width - button_spacing
    game_obj.prev_analysis_button = pygame.Rect(prev_x, y_buttons_row, button_width, button_height)
    next_x = config.SCREEN_WIDTH // 2 + turn_text_width / 2 + button_spacing
    game_obj.next_analysis_button = pygame.Rect(next_x, y_buttons_row, button_width, button_height)
    draw_button(surface, game_obj.prev_analysis_button, '<', game_obj.font_menu, mouse_pos)
    draw_text(surface, f"{game_obj.current_analysis_turn_index + 1}/{len(game_obj.analysis_results)}", game_obj.font_menu, config.WHITE, config.SCREEN_WIDTH // 2, y_buttons_row + button_height // 2, center=True)
    draw_button(surface, game_obj.next_analysis_button, '>', game_obj.font_menu, mouse_pos)
    draw_button(surface, game_obj.back_to_menu_button, 'Quay lại', game_obj.font_menu, mouse_pos)
    #draw_notification(surface, game_obj)

def draw_current_state(surface, game_obj, mouse_pos):
    """
    Hàm vẽ chính, quyết định vẽ cái gì dựa trên trạng thái game. (Phiên bản đã sửa lỗi)
    """
    
    # 1. Vẽ các thành phần chung cho các màn hình có bàn cờ
    if game_obj.game_state in ['PLAYING', 'GAME_OVER', 'PAUSED', 'ANALYSIS']:
        draw_game_board_elements(surface, game_obj)
        draw_winning_line_animation(surface, game_obj)

    # 2. Vẽ một lớp phủ mờ cho các màn hình cần làm nổi bật UI
    if game_obj.game_state in ['GAME_OVER', 'PAUSED', 'ANALYSIS']:
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

    # 3. Vẽ UI (nút bấm, text,...) cụ thể cho từng trạng thái - Đã khôi phục các elif bị thiếu
    if game_obj.game_state == 'MENU':
        draw_menu_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'CAMPAIGN':
        draw_campaign_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'PLAYING':
        draw_playing_ui(surface, game_obj)
    elif game_obj.game_state == 'GAME_OVER': # <--- ĐÃ KHÔI PHỤC
        draw_game_over_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'LEADERBOARD': # <--- ĐÃ KHÔI PHỤC
        draw_leaderboard_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'SETTINGS': # <--- ĐÃ KHÔI PHỤC
        draw_settings_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'ABOUT':
        draw_about_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'PAUSED':
        draw_pause_ui(surface, game_obj, mouse_pos)
    elif game_obj.game_state == 'ANALYSIS':
        draw_analysis_ui(surface, game_obj, mouse_pos) # Hàm này giờ chỉ còn vẽ các nút bấm

    # 4. Vẽ text phân tích LÊN TRÊN lớp phủ (nếu đang ở màn hình ANALYSIS)
    if game_obj.game_state == 'ANALYSIS':
        current_analysis = game_obj.analysis_results[game_obj.current_analysis_turn_index]
        text_info_y_start = 80
        # Vẽ tiêu đề chính
        draw_text(surface, f"Lượt: {current_analysis['turn']} (Bạn đi)", game_obj.font_title, config.WHITE, config.SCREEN_WIDTH // 2, text_info_y_start, center=True)
        
        # Vẽ các dòng text mô tả
        player_move_rect = pygame.Rect(50, text_info_y_start + 70, config.SCREEN_WIDTH - 100, 50)
        draw_text_wrapped(surface, f"Nước đi của bạn: {current_analysis['player_actual_move']}", game_obj.font_menu, config.WHITE, player_move_rect)
        
        best_move_text = f"Nước tốt nhất: {current_analysis['best_move_suggested']}"
        best_move_rect_container = pygame.Rect(50, text_info_y_start + 120, config.SCREEN_WIDTH - 100, 70)
        # Nếu bỏ lỡ cơ hội thắng thì dùng màu đỏ, nếu không thì dùng màu xanh lá
        if current_analysis['is_missed_win']:
             draw_text_wrapped(surface, best_move_text + " (BỎ LỠ CƠ HỘI THẮNG!)", game_obj.font_menu, (255, 100, 100), best_move_rect_container)
        else:
            # Màu xanh lá cây sáng để gợi ý nước đi tốt nhất
            draw_text_wrapped(surface, best_move_text, game_obj.font_menu, (100, 255, 100), best_move_rect_container)

    # 5. Vẽ thông báo (notification) đè lên trên cùng (nếu có)
    draw_notification(surface, game_obj)