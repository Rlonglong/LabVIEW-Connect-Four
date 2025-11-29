import numpy as np
import random

class Board:
    def __init__(self, table, connect=4):
        self.table = np.array(table)
        self.row, self.column = self.table.shape
        self.connect = connect
        self.valid = [c for c in range(self.column) if self.table[0, c] == 0]

    def drop_piece(self, col, piece):
        new_table = self.table.copy()
        for r in reversed(range(self.row)):
            if new_table[r, col] == 0:
                new_table[r, col] = piece
                break
        return Board(new_table, self.connect)

    def win(self, piece):
        # horizontal
        for r in range(self.row):
            for c in range(self.column - self.connect + 1):
                if all(self.table[r, c+i] == piece for i in range(self.connect)):
                    return True
        # vertical
        for r in range(self.row - self.connect + 1):
            for c in range(self.column):
                if all(self.table[r+i, c] == piece for i in range(self.connect)):
                    return True
        # diag \
        for r in range(self.row - self.connect + 1):
            for c in range(self.column - self.connect + 1):
                if all(self.table[r+i, c+i] == piece for i in range(self.connect)):
                    return True
        # diag /
        for r in range(self.connect - 1, self.row):
            for c in range(self.column - self.connect + 1):
                if all(self.table[r-i, c+i] == piece for i in range(self.connect)):
                    return True
        return False

    def terminate(self):
        return self.win(1) or self.win(2) or len(self.valid) == 0

# ---------------- Heuristic ----------------

def check_window_forwin(board, window, piece):
    if window.count(piece) == board.connect - 1 and window.count(0) == 1:
        return window.index(0)
    return None

def count_windows_forwin(board, piece):
    win_positions = []
    for r in range(board.row):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[r, c:c + board.connect])
            idx = check_window_forwin(board, window, piece)
            if idx is not None:
                win_positions.append((r, c + idx))
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column):
            window = list(board.table[r:r + board.connect, c])
            idx = check_window_forwin(board, window, piece)
            if idx is not None:
                win_positions.append((r + idx, c))
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[range(r, r + board.connect), range(c, c + board.connect)])
            idx = check_window_forwin(board, window, piece)
            if idx is not None:
                win_positions.append((r + idx, c + idx))
    for r in range(board.connect - 1, board.row):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[range(r, r - board.connect, -1), range(c, c + board.connect)])
            idx = check_window_forwin(board, window, piece)
            if idx is not None:
                win_positions.append((r - idx, c + idx))
    return win_positions

def weight_to_winning_moves(winning_moves):
    row_dict = {}
    for r, c in winning_moves:
        if r not in row_dict:
            row_dict[r] = []
        row_dict[r].append(c)
    prev_row = None
    for r in sorted(row_dict.keys()):
        if prev_row is not None and r == prev_row + 1:
            return True
        prev_row = r
    return False

def check_window_three(board, window, piece):
    values = [board.table[r][c] for r, c in window]
    if values.count(piece) == board.connect - 1 and values.count(0) == 1:
        empty_index = values.index(0)
        empty_r, empty_c = window[empty_index]
        if empty_r + 1 < board.row and board.table[empty_r + 1][empty_c] == 0:
            return True
    return False

def count_windows_three(board, piece):
    win_cnt = 0
    for r in range(board.row):
        for c in range(board.column - (board.connect - 1)):
            window = [(r, c + i) for i in range(board.connect)]
            win_cnt += check_window_three(board, window, piece)
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column):
            window = [(r + i, c) for i in range(board.connect)]
            win_cnt += check_window_three(board, window, piece)
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column - (board.connect - 1)):
            window = [(r + i, c + i) for i in range(board.connect)]
            win_cnt += check_window_three(board, window, piece)
    for r in range(board.connect - 1, board.row):
        for c in range(board.column - (board.connect - 1)):
            window = [(r - i, c + i) for i in range(board.connect)]
            win_cnt += check_window_three(board, window, piece)
    return win_cnt

def get_heuristic_strong(board):
    if board.win(1):
        return 1e12
    if board.win(2):
        return -1e12
    num_twos       = count_windows_three(board, 1)
    num_threes     = count_windows_three(board, 1)
    num_twos_opp   = count_windows_three(board, 2)
    num_threes_opp = count_windows_three(board, 2)
    forwin_bouns = weight_to_winning_moves(count_windows_forwin(board, 1))
    forwin_bouns_opp = weight_to_winning_moves(count_windows_forwin(board, 2))
    three_bouns = count_windows_three(board, 1)
    potential_bonus = 0
    cnt = 0
    for r in range(board.row):
        for c in range(board.column):
            if board.table[r][c] == 1:
                potential_bonus += 1
            elif board.table[r][c] == 2:
                potential_bonus -= 1
            else:
                cnt += 1
    score = (
        + 1e10 * forwin_bouns
        + 1e6  * three_bouns
        + 1e5  * num_threes
        + 10   * num_twos
        + cnt  * potential_bonus
        - 10   * num_twos_opp
        - 1e6  * num_threes_opp
        - 1e10 * forwin_bouns_opp
    )
    return score

# ---------------- Alpha-Beta Strong ----------------

def alphabeta_strong(board, depth, maximizingPlayer, alpha, beta, dep=4):
    if depth == 0 or board.terminate():
        return get_heuristic_strong(board), [board.valid[0]] if board.valid else [-1]

    if maximizingPlayer:
        value = -np.inf
        best_moves = []
        for col in board.valid:
            nxt_board = board.drop_piece(col, 1)
            score, _ = alphabeta_strong(nxt_board, depth-1, False, alpha, beta, dep)
            if score > value:
                value = score
                best_moves = [col]
            elif score == value:
                best_moves.append(col)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_moves
    else:
        value = np.inf
        best_moves = []
        for col in board.valid:
            nxt_board = board.drop_piece(col, 2)
            score, _ = alphabeta_strong(nxt_board, depth-1, True, alpha, beta, dep)
            if score < value:
                value = score
                best_moves = [col]
            elif score == value:
                best_moves.append(col)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_moves

# ---------------- LabVIEW Entry Function ----------------

def get_best_move(board_arr, player_piece, depth=4):
    """
    board_arr: 二維 list 或 np.array 0=空, 1=player1, 2=player2
    player_piece: int, 1 或 2
    depth: 搜尋深度
    return: 建議落子欄位 (int)
    """
    board = Board(board_arr)
    if player_piece == 1:
        _, moves = alphabeta_strong(board, depth, True, -np.inf, np.inf, depth)
    else:
        _, moves = alphabeta_strong(board, depth, False, -np.inf, np.inf, depth)
    return random.choice(moves) if moves else -1
