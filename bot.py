# bot.py
import random
import sys
from ai_logic import find_best_move # Import "bộ não" Minimax
import game_logic # Import toàn bộ module để truy cập check_win

def get_empty_cells(board, rows, cols):
    cells = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == ' ':
                cells.append((r, c))
    return cells

def get_heuristic_move(board, rows, cols, win_condition, current_eval_player):
    """Bot thông minh dựa trên quy tắc (Heuristic). current_eval_player là người đang được phân tích."""
    
    temp_board = [row[:] for row in board] # Bản sao bàn cờ

    def check_possibility(player_to_check):
        for r_empty, c_empty in get_empty_cells(temp_board, rows, cols):
            temp_board[r_empty][c_empty] = player_to_check
            if game_logic.check_win(temp_board, rows, cols, win_condition, (r_empty, c_empty), player_to_check):
                temp_board[r_empty][c_empty] = ' ' # Hoàn tác
                return (r_empty, c_empty)
            temp_board[r_empty][c_empty] = ' ' # Hoàn tác
        return None

    # 1. Tấn công: Kiểm tra xem current_eval_player có thể thắng không
    move = check_possibility(current_eval_player)
    if move: return move

    # 2. Phòng thủ: Kiểm tra xem đối thủ của current_eval_player có thể thắng không và chặn lại
    opponent_player = 'X' if current_eval_player == 'O' else 'O'
    move = check_possibility(opponent_player)
    if move: return move
    
    # 3. Chiến thuật cơ bản: Chiếm trung tâm nếu còn trống
    if rows % 2 == 1 and cols % 2 == 1:
        center_row, center_col = rows // 2, cols // 2
        if board[center_row][center_col] == ' ':
            return (center_row, center_col)

    # 4. Chiếm các góc
    corners = [(0, 0), (0, cols-1), (rows-1, 0), (rows-1, cols-1)]
    random.shuffle(corners)
    for r, c in corners:
        if board[r][c] == ' ':
            return (r, c)

    # 5. Đi vào một ô trống gần một quân cờ đã có
    candidate_moves = []
    empty_cells = get_empty_cells(board, rows, cols)
    for r_empty, c_empty in empty_cells:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                r_neighbor, c_neighbor = r_empty + dr, c_empty + dc
                if 0 <= r_neighbor < rows and 0 <= c_neighbor < cols and board[r_neighbor][c_neighbor] != ' ':
                    candidate_moves.append((r_empty, c_empty))
                    break
            if candidate_moves and candidate_moves[-1] == (r_empty, c_empty):
                break
    
    if candidate_moves:
        return random.choice(candidate_moves)

    # 6. Nếu không có nước đi chiến lược nào, đi ngẫu nhiên
    return random.choice(empty_cells)


def get_bot_move(board, difficulty, rows, cols, win_condition, is_analysis=False, analysis_player=None):
    """
    Quyết định nước đi cho bot hoặc cho mục đích phân tích.
    Args:
        board (list[list[str]]): Bàn cờ hiện tại.
        difficulty (str): Độ khó của bot ('easy', 'medium', 'hard', 'insane').
        rows (int): Số hàng của bàn cờ.
        cols (int): Số cột của bàn cờ.
        win_condition (int): Số quân liên tiếp để thắng.
        is_analysis (bool): True nếu hàm được gọi cho mục đích phân tích nước đi.
        analysis_player (str, optional): Ký tự của người chơi cần phân tích ('X' hoặc 'O'). 
                                        Chỉ dùng khi is_analysis=True.
    Returns:
        tuple (row, col) hoặc None: Nước đi được chọn.
    """
    empty_cells = get_empty_cells(board, rows, cols)
    if not empty_cells: return None

    # Xác định người chơi hiện tại mà bot (hoặc phân tích) đang cố gắng đi nước
    current_eval_player = analysis_player if is_analysis else 'O' # Nếu phân tích thì đi cho player, nếu không thì đi cho bot O
    
    if difficulty == 'easy':
        return random.choice(empty_cells)
    
    elif difficulty == 'medium':
        # Độ khó Medium: Có 20% đi ngẫu nhiên, còn lại dùng heuristic
        if random.random() < 0.2 and not is_analysis: # Không đi ngẫu nhiên khi phân tích
            return random.choice(empty_cells)
        return get_heuristic_move(board, rows, cols, win_condition, current_eval_player)
        
    elif difficulty == 'hard':
        # Độ khó Hard: Luôn dùng heuristic
        return get_heuristic_move(board, rows, cols, win_condition, current_eval_player)
        
    elif difficulty == 'insane':
        # Độ khó cao nhất sẽ dùng Minimax.
        # Rất chậm trên bàn cờ lớn hơn 4x4.
        print(f"Bot ({difficulty}) đang tính toán nước đi tối ưu cho {current_eval_player}...")
        # find_best_move trong ai_logic cần biết ai đang đi cờ
        # Nếu is_analysis, thì Minimax cần tối đa hóa cho 'X'
        return find_best_move(board, win_condition, current_eval_player)

    # Mặc định trả về nước đi ngẫu nhiên
    return random.choice(empty_cells)