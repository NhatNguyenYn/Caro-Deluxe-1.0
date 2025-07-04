# ai_logic.py
# Chứa thuật toán Minimax với tối ưu hóa Alpha-Beta Pruning.

WIN_SCORE = 1000 # Tăng điểm số để dễ phân biệt
LOSE_SCORE = -1000
DRAW_SCORE = 0

def evaluate(board, win_condition, current_eval_player):
    """
    Đánh giá trạng thái hiện tại của bàn cờ.
    Hàm này được gọi khi game đã kết thúc hoặc tại độ sâu giới hạn.
    current_eval_player là người chơi mà minimax đang cố gắng tối đa hóa.
    """
    rows, cols = len(board), len(board[0])
    
    def check_line(cells):
        if all(cell == current_eval_player for cell in cells): return WIN_SCORE
        opponent_player = 'X' if current_eval_player == 'O' else 'O'
        if all(cell == opponent_player for cell in cells): return LOSE_SCORE
        return None

    # Hàng ngang
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            score = check_line([board[r][c+i] for i in range(win_condition)])
            if score is not None: return score
            
    # Hàng dọc
    for c in range(cols):
        for r in range(rows - win_condition + 1):
            score = check_line([board[r+i][c] for i in range(win_condition)])
            if score is not None: return score
            
    # Đường chéo chính (\)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            score = check_line([board[r+i][c+i] for i in range(win_condition)])
            if score is not None: return score
            
    # Đường chéo phụ (/)
    for r in range(rows - win_condition + 1):
        for c in range(win_condition - 1, cols):
            score = check_line([board[r+i][c-i] for i in range(win_condition)])
            if score is not None: return score
            
    return DRAW_SCORE

def is_moves_left(board):
    for row in board:
        if ' ' in row: return True
    return False

def minimax(board, depth, is_maximizing, alpha, beta, win_condition, current_eval_player):
    """Hàm đệ quy Minimax."""
    score = evaluate(board, win_condition, current_eval_player)

    if score == WIN_SCORE: return score - depth
    if score == LOSE_SCORE: return score + depth
    if not is_moves_left(board): return DRAW_SCORE
    
    # Giới hạn độ sâu. Rất quan trọng cho bàn cờ lớn hơn 3x3.
    # Đối với 3x3, có thể bỏ giới hạn depth hoặc để rất cao.
    # Với bàn cờ 5x5 và win_condition = 4, depth 4-5 là hợp lý.
    if depth > 4: return 0 # Giới hạn độ sâu, có thể điều chỉnh

    # Nếu đang là lượt của người chơi Tối đa hóa (current_eval_player)
    if is_maximizing:
        best = -float('inf') # Sử dụng âm vô cùng
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == ' ':
                    board[r][c] = current_eval_player
                    best = max(best, minimax(board, depth + 1, not is_maximizing, alpha, beta, win_condition, current_eval_player))
                    board[r][c] = ' ' # Hoàn tác
                    alpha = max(alpha, best)
                    if beta <= alpha: break
            if beta <= alpha: break # Phải có break kép
        return best
    # Nếu đang là lượt của người chơi Tối thiểu hóa (Đối thủ của current_eval_player)
    else:
        opponent_player = 'X' if current_eval_player == 'O' else 'O'
        best = float('inf') # Sử dụng dương vô cùng
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == ' ':
                    board[r][c] = opponent_player
                    best = min(best, minimax(board, depth + 1, not is_maximizing, alpha, beta, win_condition, current_eval_player))
                    board[r][c] = ' ' # Hoàn tác
                    beta = min(beta, best)
                    if beta <= alpha: break
            if beta <= alpha: break # Phải có break kép
        return best

def find_best_move(board, win_condition, current_player_for_analysis):
    """
    Hàm chính để tìm nước đi tốt nhất cho người chơi 'current_player_for_analysis'.
    """
    best_val = -float('inf')
    best_move = None
    
    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == ' ':
                board[r][c] = current_player_for_analysis # Đặt quân của người chơi đang được phân tích
                move_val = minimax(board, 0, False, -float('inf'), float('inf'), win_condition, current_player_for_analysis)
                board[r][c] = ' ' # Hoàn tác
                
                if move_val > best_val:
                    best_move = (r, c)
                    best_val = move_val
    return best_move