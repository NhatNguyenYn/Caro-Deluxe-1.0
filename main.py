# main.py - Phiên bản có Phân tích lỗi AI, Thông báo, Screen Shake và Additional Message

import pygame
import sys
import time
import math
import os

import renderer
import game_logic
import config
from levels import LEVELS
import bot
import utils
from sound_manager import SoundManager
import login_screen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Caro Deluxe - AI Insane Mode")
        self.clock = pygame.time.Clock()
        
        self.sound_manager = SoundManager()

        self.notification = None 
        self.notification_duration = 2.0 # Thời gian hiển thị notification (giây)

        self.current_theme_name = "light"
        self.apply_theme(self.current_theme_name)
        
        self.font_title, self.font_menu, self.font_status = None, None, None
        self.load_assets_fonts()
        
        self.username = login_screen.get_username_input(
            self.screen, self.font_title, self.font_menu, self.font_status, self.sound_manager, self.clock
        )
        
        self.game_state = 'MENU'
        self.game_mode = None
        self.difficulty = None
        
        self.board = []
        self.current_player = 'X'
        self.winner = None
        self.last_move = None
        self.game_over = False
        self.additional_message = None  # Thêm thuộc tính cho dòng chữ phụ

        self.board_rows = config.DEFAULT_BOARD_ROWS
        self.board_cols = config.DEFAULT_BOARD_COLS
        self.win_condition = config.DEFAULT_WIN_CONDITION
        self.square_size = config.SCREEN_WIDTH // self.board_cols
        self.line_width = max(1, 10 - self.board_rows // 2)

        self.is_animating = False
        self.anim_progress = 0.0
        self.anim_pos = None
        self.anim_player = None
        self.winning_line_data = None
        self.winning_anim_progress = 0.0
        self.winning_anim_duration = 0.5
        
        self.move_history = []
        self.analysis_results = []
        self.current_analysis_turn_index = 0
        
        self.notification = None
        self.shake_timer = 0.0
        
        self.x_img_orig, self.o_img_orig = None, None
        self.x_img, self.o_img = None, None
        self.load_assets_images()
        
        # --- NÚT BẤM VÀ VỊ TRÍ ---
        self.input_box = pygame.Rect(100, config.SCREEN_HEIGHT // 2 - 25, 400, 50)
        self.pvp_button = pygame.Rect(150, 200, 300, 60)
        self.campaign_button = pygame.Rect(150, 280, 300, 60)
        self.leaderboard_button = pygame.Rect(150, 360, 300, 60)
        self.settings_button = pygame.Rect(150, 440, 300, 60)
        self.about_button = pygame.Rect(150, 520, 300, 60)
        self.load_game_button = pygame.Rect(150, 120, 300, 60) # Nút tải game (trong menu)

        self.play_again_button = pygame.Rect(80, config.SCREEN_HEIGHT - 150, 220, 60)
        self.back_to_menu_button = pygame.Rect(320, config.SCREEN_HEIGHT - 150, 200, 60)
        self.level_buttons = [] # Sẽ được tạo trong renderer
        self.music_toggle_button = pygame.Rect(350, 190, 150, 50)
        self.music_volume_slider_rect = pygame.Rect(350, 285, 200, 10)
        self.sfx_volume_slider_rect = pygame.Rect(350, 365, 200, 10)
        self.is_dragging_slider = None # Cho slider
        self.pause_buttons = {} # Cho Pause Menu (dictionary sẽ được fill bởi renderer)
        self.theme_toggle_button = pygame.Rect(350, 430, 150, 50) # Cho Settings
        self.save_game_button = pygame.Rect(150, config.SCREEN_HEIGHT // 2 + 190, 300, 60) # Cho Pause Menu

        # Các nút cho Pause Menu (cần khởi tạo kích thước chính xác)
        self.resume_button = pygame.Rect(0, 0, 300, 60) 
        self.main_menu_button = pygame.Rect(0, 0, 300, 60)
        self.quit_game_button = pygame.Rect(0, 0, 300, 60)

        # === THÊM KHỞI TẠO NÚT ANALYZE_BUTTON NÀY VÀO __init__ ===
        self.analyze_button = pygame.Rect(150, config.SCREEN_HEIGHT // 2 + 30, 300, 60) # Nút Phân tích trận
        self.next_analysis_button = pygame.Rect(0, 0, 100, 60) # Nút > cho phân tích
        self.prev_analysis_button = pygame.Rect(0, 0, 100, 60) # Nút < cho phân tích
        # ==========================================================

        self.sound_manager.play_music()

    def start_notification(self, message):
        self.notification = (message, self.notification_duration)

    def apply_theme(self, theme_name):
        theme = config.THEMES.get(theme_name, config.THEMES["light"])
        config.BG_COLOR, config.LINE_COLOR, config.BUTTON_HOVER_COLOR = theme["BG_COLOR"], theme["LINE_COLOR"], theme["BUTTON_HOVER_COLOR"]
        config.WHITE, config.BLACK, config.TEXT_COLOR = theme["WHITE"], theme["BLACK"], theme["TEXT_COLOR"]
        config.X_COLOR, config.O_COLOR = theme["X_COLOR"], theme["O_COLOR"]
        config.WINNING_LINE_COLOR, config.LAST_MOVE_HIGHLIGHT_COLOR = theme["WINNING_LINE_COLOR"], theme["LAST_MOVE_HIGHLIGHT_COLOR"]
        self.current_theme_name = theme_name
        self.sound_manager.update_volumes()

    def load_assets_fonts(self):
        try:
            if config.FONT_PATH:
                self.font_title = pygame.font.Font(config.FONT_PATH, 60)
                self.font_menu = pygame.font.Font(config.FONT_PATH, 40)
                self.font_status = pygame.font.Font(config.FONT_PATH, 30)
            else:
                raise FileNotFoundError
        except (FileNotFoundError, pygame.error):
            self.font_title = pygame.font.Font(None, 80)
            self.font_menu = pygame.font.Font(None, 50)
            self.font_status = pygame.font.Font(None, 40)
    
    def load_assets_images(self):
        try:
            self.x_img_orig = pygame.image.load('assets/images/x.png').convert_alpha()
            self.o_img_orig = pygame.image.load('assets/images/o.png').convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.x_img_orig, self.o_img_orig = None, None

    def setup_board(self, rows, cols, win_condition, difficulty=None, mode=None):
        utils.delete_save_game() # Xóa file save cũ vì chúng ta bắt đầu ván mới
        print("Bắt đầu ván mới, file save cũ (nếu có) đã được xóa.")

        self.board_rows, self.board_cols, self.win_condition = rows, cols, win_condition
        self.square_size = config.SCREEN_WIDTH // self.board_cols
        self.line_width = max(1, 10 - self.board_rows // 2)
        self.difficulty, self.game_mode = difficulty, mode
        if self.x_img_orig and self.o_img_orig:
            img_size = int(self.square_size * 0.8)
            self.x_img = pygame.transform.smoothscale(self.x_img_orig, (img_size, img_size))
            self.o_img = pygame.transform.smoothscale(self.o_img_orig, (img_size, img_size))
        else:
            self.x_img, self.o_img = None, None
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.current_player, self.winner, self.last_move, self.game_over = 'X', None, None, False
        self.game_state = 'PLAYING'
        self.winning_line_data, self.winning_anim_progress = None, 0.0
        self.move_history = []
        self.analysis_results = []
        self.current_analysis_turn_index = 0
        self.notification = None
        self.shake_timer = 0.0
        self.additional_message = None  # Đặt lại dòng chữ phụ

    def show_notification(self, message, duration=2.0):
        self.notification = (message, duration)

    def save_current_game(self): # Sửa lại để dùng start_notification
        game_state_data = {
            "board": self.board, "current_player": self.current_player, "game_mode": self.game_mode,
            "difficulty": self.difficulty, "board_rows": self.board_rows, "board_cols": self.board_cols,
            "win_condition": self.win_condition, "username": self.username, "theme": self.current_theme_name,
            "move_history": self.move_history
        }
        if utils.save_game_state(game_state_data):
            self.start_notification("Đã lưu game thành công!")
            return True
        else:
            self.start_notification("Lưu game thất bại!")
            return False

    def load_saved_game(self):
        """Tải game đã lưu. SẼ KHÔNG XÓA FILE SAU KHI TẢI.""" # Cập nhật chú thích
        saved_data = utils.load_game_state()
        if saved_data:
            # === BỎ ĐI DÒNG XÓA FILE Ở ĐÂY ===
            # utils.delete_save_game()  <-- XÓA HOẶC CHÚ THÍCH DÒNG NÀY

            self.board = saved_data["board"]
            self.current_player = saved_data["current_player"]
            self.game_mode = saved_data["game_mode"]
            self.difficulty = saved_data["difficulty"]
            self.board_rows = saved_data["board_rows"]
            self.board_cols = saved_data["board_cols"]
            self.win_condition = saved_data["win_condition"]
            # username không nên được load lại, giữ nguyên người đang đăng nhập
            # self.username = saved_data["username"] 

            self.apply_theme(saved_data.get("theme", "light"))
            
            self.square_size = config.SCREEN_WIDTH // self.board_cols
            self.line_width = max(1, 10 - self.board_rows // 2)
            
            if self.x_img_orig and self.o_img_orig:
                img_size = int(self.square_size * 0.8)
                self.x_img = pygame.transform.smoothscale(self.x_img_orig, (img_size, img_size))
                self.o_img = pygame.transform.smoothscale(self.o_img_orig, (img_size, img_size))
            
            self.game_over = False
            self.winner = None
            self.last_move = None
            self.game_state = 'PLAYING'

            # Reset các trạng thái animation từ ván trước
            self.winning_line_data = None
            self.winning_anim_progress = 0.0
            self.is_animating = False
            
            self.move_history = saved_data.get("move_history", [])
            # Lấy last_move từ nước đi cuối cùng trong lịch sử (nếu có)
            if self.move_history:
                self.last_move = self.move_history[-1]['move']
                
            self.analysis_results = []
            self.current_analysis_turn_index = 0
            
            self.start_notification("Đã tải game thành công!")
            return True

        self.start_notification("Không tìm thấy file lưu game!")
        return False

    def start_animation(self, row, col, player):
        self.is_animating, self.anim_progress = True, 0.0
        self.anim_pos, self.anim_player = (row, col), player
        self.sound_manager.play('place')

    def update_animation(self):
        if not self.is_animating:
            if self.game_over and self.winner and self.winning_line_data:
                self.winning_anim_progress += 1 / (self.winning_anim_duration * self.clock.get_fps())
                if self.winning_anim_progress >= 1.0:
                    self.winning_anim_progress = 1.0
                coords, player, _ = self.winning_line_data
                self.winning_line_data = (coords, player, self.winning_anim_progress)
            return
        self.anim_progress = min(1.0, self.anim_progress + 0.1)
        row, col = self.anim_pos
        center_x, center_y = col*self.square_size+self.square_size//2, row*self.square_size+self.square_size//2
        progress_eased = 1 - (1 - self.anim_progress)**3
        current_size = int(int(self.square_size*0.8)*progress_eased)
        if current_size<=0:
            return
        img_to_draw = self.x_img if self.anim_player=='X' else self.o_img
        if img_to_draw:
            scaled_img = pygame.transform.smoothscale(img_to_draw, (current_size, current_size))
            rect = scaled_img.get_rect(center=(center_x, center_y))
            self.screen.blit(scaled_img, rect)
        if self.anim_progress >= 1.0:
            self.is_animating = False
            self.process_turn()

    def handle_click(self, pos):
        if self.game_state == 'PLAYING' and not self.game_over and not self.is_animating:
            if pos[1] < self.board_rows * self.square_size:
                col = pos[0] // self.square_size
                row = pos[1] // self.square_size
                if 0 <= row < self.board_rows and 0 <= col < self.board_cols and self.board[row][col] == ' ':
                    self.start_animation(row, col, self.current_player)

    def process_turn(self):
        row, col = self.anim_pos
        self.last_move = (row, col)
        self.move_history.append({
            'board': [r[:] for r in self.board],
            'move': (row, col),
            'player': self.current_player,
            'rows': self.board_rows,
            'cols': self.board_cols
        })
        self.board[row][col] = self.anim_player
        win_coords = game_logic.check_win(self.board, self.board_rows, self.board_cols, self.win_condition, self.last_move, self.anim_player)
        if win_coords:
            self.winner = self.anim_player
            self.winning_line_data = (win_coords, self.winner, 0.0)
            self.end_game()
        elif game_logic.check_draw(self.board, self.board_rows, self.board_cols):
            self.winner = None
            self.end_game()
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def end_game(self):
        """Kết thúc ván đấu và cập nhật bảng xếp hạng. Thêm phân tích sau trận."""
        self.game_over = True
        self.game_state = 'GAME_OVER'
        # Vì game đã kết thúc, file save cho game này không còn cần thiết nữa.
        utils.delete_save_game()
        print("Game kết thúc, file save đã được xóa.")
        # =========================================
        player1, player2 = None, None
        if self.game_mode == 'pvc': player1, player2 = self.username, f'Bot ({self.difficulty})'
        elif self.game_mode == 'pvp': player1, player2 = "Player 1", "Player 2"
        
        if not player1: return

        if self.winner == 'X':
            utils.update_leaderboard(player1, 'win'); utils.update_leaderboard(player2, 'loss')
            if self.game_mode == 'pvc': self.sound_manager.play('win')
        elif self.winner == 'O':
            utils.update_leaderboard(player1, 'loss'); utils.update_leaderboard(player2, 'win')
            if self.game_mode == 'pvc': self.sound_manager.play('lose')
        else: # Hòa
            utils.update_leaderboard(player1, 'draw'); utils.update_leaderboard(player2, 'draw')
            self.sound_manager.play('lose')

        # === ĐÃ LOẠI BỎ LOGIC XÓA SAVE GAME TẠI ĐÂY ===
        # File savegame.json sẽ được xóa khi load_saved_game() thành công.
        # Hoặc không có file savegame.json nào nếu đây là ván mới.
        # Vì vậy không cần kiểm tra và xóa ở đây nữa.
        # ==============================================

        # PHÂN TÍCH NƯỚC ĐI SAU TRẬN (Chỉ nếu chơi với máy và có lịch sử)
        if self.game_mode == 'pvc' and self.move_history:
            print("Đang phân tích nước đi của bạn...")
            import os # Cần import os để kiểm tra file
            self.analysis_results = game_logic.analyze_player_moves(
                self.move_history,
                self.difficulty,
                'heuristic', # Giả định bot là heuristic để phân tích
                'X', 'O',
                self.board_rows,
                self.board_cols,
                self.win_condition
            )
            self.current_analysis_turn_index = 0
            print(f"Tìm thấy {len(self.analysis_results)} nước đi có thể cải thiện.")

    def run(self):
        while True:
            self.screen.fill(config.BG_COLOR) # Dòng này từ lần sửa trước, giữ nguyên

            mouse_pos = pygame.mouse.get_pos()
            self.handle_events(mouse_pos)
            
            if self.notification:
                message, timer = self.notification
                timer -= 1 / self.clock.get_fps()
                self.notification = (message, timer) if timer > 0 else None
            
            # === SỬA LẠI KHỐI NÀY ===
            # Thay vì viết logic ở đây, chúng ta gọi hàm đã có sẵn
            self.handle_bot_turn()
            # =========================
            
            # Giữ nguyên các dòng này
            renderer.draw_current_state(self.screen, self, mouse_pos)
            self.update_animation()
            pygame.display.update()
            self.clock.tick(60)
            
    def handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == 'PLAYING' and event.key == pygame.K_ESCAPE:
                    self.sound_manager.play('click'); self.game_state = 'PAUSED'
                elif self.game_state == 'PAUSED' and event.key == pygame.K_ESCAPE:
                    self.sound_manager.play('click'); self.game_state = 'PLAYING'
                
            if self.game_state == 'SETTINGS': # Xử lý sự kiện cho Settings
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_volume_slider_rect.collidepoint(event.pos): self.is_dragging_slider = 'music'
                    elif self.sfx_volume_slider_rect.collidepoint(event.pos): self.is_dragging_slider = 'sfx'
                elif event.type == pygame.MOUSEBUTTONUP: self.is_dragging_slider = None
                elif event.type == pygame.MOUSEMOTION and self.is_dragging_slider:
                    if self.is_dragging_slider == 'music': new_volume = (mouse_pos[0] - self.music_volume_slider_rect.x) / self.music_volume_slider_rect.width; self.sound_manager.set_music_volume(new_volume)
                    elif self.is_dragging_slider == 'sfx': new_volume = (mouse_pos[0] - self.sfx_volume_slider_rect.x) / self.sfx_volume_slider_rect.width; self.sound_manager.set_sfx_volume(new_volume)
                if event.type == pygame.MOUSEBUTTONDOWN and self.music_toggle_button.collidepoint(mouse_pos):
                    if pygame.mixer.music.get_busy(): self.sound_manager.stop_music()
                    else: self.sound_manager.play_music()

            # --- Xử lý sự kiện theo trạng thái Game (Click chuột) ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == 'MENU':
                    if self.pvp_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.setup_board(config.DEFAULT_BOARD_ROWS, config.DEFAULT_BOARD_COLS, config.DEFAULT_WIN_CONDITION, mode='pvp')
                    elif self.campaign_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'CAMPAIGN'
                    elif self.leaderboard_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'LEADERBOARD'
                    elif self.settings_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'SETTINGS'
                    elif self.about_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'ABOUT'
                    elif self.load_game_button.collidepoint(mouse_pos): # Tải game
                        self.sound_manager.play('click')
                        if self.load_saved_game(): print("Đã tải game thành công!")
                        else: print("Không có game đã lưu hoặc tải thất bại.")
                        
                elif self.game_state == 'CAMPAIGN':
                    if self.back_to_menu_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = "MENU"
                    for i, button in enumerate(self.level_buttons):
                        if button.collidepoint(mouse_pos):
                            self.sound_manager.play('click')
                            level = LEVELS[i]
                            self.setup_board(level["rows"], level["cols"], level["win_condition"], level["difficulty"], 'pvc')
                            break

                elif self.game_state == 'PLAYING':
                    if not self.game_over and not self.is_animating:
                        if self.game_mode == 'pvp' or (self.game_mode == 'pvc' and self.current_player == 'X'): self.handle_click(mouse_pos)
                
                elif self.game_state == 'GAME_OVER':
                    if self.analyze_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        if self.analysis_results:  # Điều kiện này vẫn đúng, vì chỉ có PvC mới có results
                            self.game_state = 'ANALYSIS'
                        else:
                            # THAY DÒNG print BẰNG DÒNG NÀY
                            self.start_notification("Only for play with BOT")
                    elif self.play_again_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        self.reset_game()
                    elif self.back_to_menu_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        self.game_state = 'MENU'
            
                elif self.game_state == 'LEADERBOARD':
                    if self.back_to_menu_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'MENU'

                elif self.game_state == 'SETTINGS':
                    if self.back_to_menu_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'MENU'
                    elif self.theme_toggle_button.collidepoint(mouse_pos):
                        next_theme = "dark" if self.current_theme_name == "light" else "light"
                        self.apply_theme(next_theme)
                        self.sound_manager.play('click')
                
                elif self.game_state == 'ABOUT':
                    if self.back_to_menu_button.collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'MENU'

                elif self.game_state == 'PAUSED':
                    if self.pause_buttons['resume'].collidepoint(mouse_pos): self.sound_manager.play('click'); self.game_state = 'PLAYING'
                    elif self.pause_buttons['main_menu'].collidepoint(mouse_pos):
                        self.sound_manager.play('click'); self.game_state = 'MENU'
                        self.board_rows, self.board_cols, self.win_condition = config.DEFAULT_BOARD_ROWS, config.DEFAULT_BOARD_COLS, config.DEFAULT_WIN_CONDITION
                        self.square_size = config.SCREEN_WIDTH // self.board_cols; self.line_width = max(1, 10 - self.board_rows // 2)
                        self.board = [[' ' for _ in range(self.board_cols)] for _ in range(self.board_rows)]; self.current_player = 'X'
                        self.winner, self.last_move, self.game_over = None, None, False; self.is_animating = False
                        self.winning_line_data, self.game_mode, self.difficulty = None, None, None
                        self.move_history, self.analysis_results, self.current_analysis_turn_index = [], [], 0
                        print("Returned to Main Menu from Pause. Game state cleared.")
                    elif self.pause_buttons['quit'].collidepoint(mouse_pos): pygame.quit(); sys.exit() # Không play sound vì thoát ngay
                    elif self.save_game_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        if self.save_current_game(): print("Game đã được lưu thành công!")
                        else: print("Lưu game thất bại.")
                
                elif self.game_state == 'ANALYSIS':
                    if self.back_to_menu_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        self.game_state = 'GAME_OVER'
                    elif self.next_analysis_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        self.current_analysis_turn_index = min(len(self.analysis_results) - 1, self.current_analysis_turn_index + 1)
                    elif self.prev_analysis_button.collidepoint(mouse_pos):
                        self.sound_manager.play('click')
                        self.current_analysis_turn_index = max(0, self.current_analysis_turn_index - 1)
            
            elif event.type == pygame.MOUSEBUTTONUP: self.is_dragging_slider = None
            elif event.type == pygame.MOUSEMOTION and self.is_dragging_slider:
                if self.is_dragging_slider == 'music': new_volume = (mouse_pos[0] - self.music_volume_slider_rect.x) / self.music_volume_slider_rect.width; self.sound_manager.set_music_volume(new_volume)
                elif self.is_dragging_slider == 'sfx': new_volume = (mouse_pos[0] - self.sfx_volume_slider_rect.x) / self.sfx_volume_slider_rect.width; self.sound_manager.set_sfx_volume(new_volume)

    def handle_bot_turn(self):
        if self.game_state == 'PLAYING' and self.game_mode == 'pvc' and self.current_player == 'O' and not self.game_over and not self.is_animating:
            #pygame.display.update()
            time.sleep(0.5)
            move = bot.get_bot_move(self.board, self.difficulty, self.board_rows, self.board_cols, self.win_condition)
            if move:
                self.start_animation(move[0], move[1], 'O')
                
if __name__ == "__main__":
    game = Game()
    game.run()