# game_logic.py
# Chứa các hàm logic thuần túy liên quan đến quy tắc trò chơi.

def check_win(board, board_rows, board_cols, win_condition, last_move, player):
    """
    Kiểm tra thắng thua và trả về danh sách tọa độ các quân cờ thắng
    nếu có, nếu không thì trả về False.
    """
    if not last_move:
        return False
        
    last_row, last_col = last_move
    # Các hướng cần kiểm tra: (dr, dc)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Ngang, Dọc, Chéo chính, Chéo phụ
    
    for dr, dc in directions:
        count = 1
        winning_coords = [(last_row, last_col)] # Bắt đầu đếm từ quân vừa đặt
        
        # Đếm xuôi theo hướng
        for i in range(1, win_condition):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < board_rows and 0 <= c < board_cols and board[r][c] == player:
                count += 1
                winning_coords.append((r, c))
            else:
                break
        
        # Đếm ngược theo hướng
        for i in range(1, win_condition):
            r, c = last_row - i * dr, last_col - i * dc
            if 0 <= r < board_rows and 0 <= c < board_cols and board[r][c] == player:
                count += 1
                winning_coords.insert(0, (r, c)) # Thêm vào đầu danh sách để giữ thứ tự đúng
            else:
                break
        
        if count >= win_condition:
            return winning_coords # Trả về danh sách tọa độ các quân cờ thắng
            
    return False

def check_draw(board, board_rows, board_cols):
    """Kiểm tra xem bàn cờ đã hòa chưa."""
    for r in range(board_rows):
        for c in range(board_cols):
            if board[r][c] == ' ':
                return False
    return True

def analyze_player_moves(move_history, bot_difficulty, bot_type, player_char, opponent_char, initial_rows, initial_cols, win_condition):
    """
    Phân tích các nước đi của người chơi trong lịch sử trận đấu.
    initial_rows, initial_cols là kích thước bàn cờ ban đầu của trận đấu.
    """
    analysis_results = []
    
    from bot import get_bot_move # Import tại đây để tránh import vòng

    # Lặp qua lịch sử các trạng thái bàn cờ trước nước đi của người chơi
    # (Chỉ phân tích nước đi của người chơi, tức là các lượt chẵn trong move_history)
    for i in range(0, len(move_history), 2):
        if i >= len(move_history): break

        board_state_before_player_move = move_history[i]['board']
        player_actual_move = move_history[i]['move'] # (row, col)

        # Lấy kích thước bàn cờ cho nước đi này từ history
        current_rows = move_history[i].get('rows', initial_rows)
        current_cols = move_history[i].get('cols', initial_cols)

        temp_board = [row[:] for row in board_state_before_player_move]

        # Yêu cầu bot tìm nước đi tốt nhất cho người chơi (player_char)
        best_move_for_player = get_bot_move(
            temp_board, bot_difficulty, current_rows, current_cols, win_condition,
            is_analysis=True, analysis_player=player_char
        )
        
        # So sánh nước đi thực tế của người chơi với nước đi tốt nhất mà bot tìm được
        if best_move_for_player and player_actual_move != best_move_for_player:
            temp_board_after_best_move = [row[:] for row in board_state_before_player_move]
            
            # === SỬA LỖI TẠI ĐÂY: Truy cập phần tử list bằng chỉ số số nguyên ===
            row_best, col_best = best_move_for_player # Giải nén tuple
            temp_board_after_best_move[row_best][col_best] = player_char
            # ===================================================================
            
            win_check = check_win(temp_board_after_best_move, current_rows, current_cols, win_condition, best_move_for_player, player_char)

            analysis_results.append({
                "turn": i // 2 + 1,
                "board_before_move": board_state_before_player_move,
                "player_actual_move": player_actual_move,
                "best_move_suggested": best_move_for_player,
                "is_missed_win": bool(win_check),
                "rows": current_rows,
                "cols": current_cols
            })
    return analysis_results