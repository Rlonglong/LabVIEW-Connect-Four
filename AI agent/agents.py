import numpy as np
import random


'''
=====================================
Board Class
=====================================
This class represents the Connect-4 board and all game-related mechanics.

Responsibilities:
- Store the board state
- Apply and undo moves
- Detect wins and terminal states
- Enumerate all possible 4-cell windows with exact coordinates
'''
class Board:
    def __init__(self, table, connect=4):
        # Convert input board to numpy array for efficient slicing
        self.table = np.array(table)
        self.row, self.column = self.table.shape
        self.connect = connect
        
    # Check if a column can accept a new piece
    # A column is valid if its top cell is empty
    def is_valid_move(self, col):
        return self.table[self.row - 1, col] == 0

    # Return all columns that are currently playable
    def get_valid_locations(self):
        return [c for c in range(self.column) if self.is_valid_move(c)]

    # Drop a piece into a column following gravity rules
    # Returns the row index where the piece lands
    def make_move(self, col, piece):
        for r in range(self.row):
            if self.table[r, col] == 0:
                self.table[r, col] = piece
                return r
        return -1

    # Undo a move by clearing the specified cell
    def undo_move(self, col, row):
        self.table[row, col] = 0

    # Check whether the given player has won
    def win(self, piece):
        # Horizontal check
        for r in range(self.row):
            for c in range(self.column - self.connect + 1):
                if np.all(self.table[r, c:c+self.connect] == piece):
                    return True

        # Vertical check
        for r in range(self.row - self.connect + 1):
            for c in range(self.column):
                if np.all(self.table[r:r+self.connect, c] == piece):
                    return True

        # Positive diagonal (\)
        for r in range(self.row - self.connect + 1):
            for c in range(self.column - self.connect + 1):
                if all(self.table[r+i, c+i] == piece for i in range(self.connect)):
                    return True

        # Negative diagonal (/)
        for r in range(self.connect - 1, self.row):
            for c in range(self.column - self.connect + 1):
                if all(self.table[r-i, c+i] == piece for i in range(self.connect)):
                    return True

        return False

    # Terminal state: someone wins or board is full
    def terminate(self):
        return self.win(1) or self.win(2) or len(self.get_valid_locations()) == 0


    '''
    Generator that enumerates all possible 4-cell windows on the board.

    Each yielded element contains:
    - window values (list or array of length 4)
    - exact (row, col) coordinates of each cell

    This is crucial for:
    - Heuristic evaluation
    - Identifying exact winning/blocking positions
    '''
    def get_all_windows_with_coords(self):

        # Horizontal windows
        for r in range(self.row):
            for c in range(self.column - self.connect + 1):
                coords = [(r, c+i) for i in range(self.connect)]
                yield self.table[r, c:c+self.connect], coords
        
        # Vertical windows
        for r in range(self.row - self.connect + 1):
            for c in range(self.column):
                coords = [(r+i, c) for i in range(self.connect)]
                yield self.table[r:r+self.connect, c], coords
        
        # Positive diagonal (\)
        for r in range(self.row - self.connect + 1):
            for c in range(self.column - self.connect + 1):
                coords = [(r+i, c+i) for i in range(self.connect)]
                val = [self.table[r+i, c+i] for i in range(self.connect)]
                yield val, coords
        
        # Negative diagonal (/)
        for r in range(self.connect - 1, self.row):
            for c in range(self.column - self.connect + 1):
                coords = [(r-i, c+i) for i in range(self.connect)]
                val = [self.table[r-i, c+i] for i in range(self.connect)]
                yield val, coords


'''
=====================================
is_playable
=====================================
Determine whether a specific cell (r, c) is playable *right now*.

In Connect-4, a cell is playable if and only if:
- It is the lowest empty cell in its column

This function fixes a common mistake:
Checking the cell below is NOT sufficient for horizontal or diagonal threats.
'''
def is_playable(board, r, c):
    for rr in range(board.row):
        if board.table[rr, c] == 0:
            return rr == r
    return False


# ---------------- Heuristic ----------------

'''
This function is currently unused.

Originally intended to:
- Analyze patterns among multiple winning spots
- Detect special double-threat structures

The actual double-threat logic has been moved
into get_heuristic_strong using set size checks.
'''
def weight_to_winning_moves(winning_moves_set):
    row_dict = {}
    for r, c in winning_moves_set:
        if c not in row_dict:
            row_dict[c] = []
        row_dict[c].append(r)
    return False


'''
=====================================
get_heuristic_strong
=====================================
Static evaluation function for the board.

Core ideas:
- Immediate wins dominate all other considerations
- Detect "true" winning threats (playable 3-in-a-row)
- Penalize opponent threats more aggressively than
  rewarding own potential
- Distinguish between playable and floating patterns

This heuristic is designed specifically for minimax.
'''
def get_heuristic_strong(board):
    # Hard terminal evaluation
    if board.win(1): return 1e12
    if board.win(2): return -1e12

    # Track immediate winning positions
    winning_spots_p1 = set()
    winning_spots_p2 = set()

    # Track non-playable (floating) threats
    floating_threes_p1 = 0
    floating_threes_p2 = 0

    # Track weaker structures
    num_twos = 0
    num_twos_opp = 0
    potential_bonus = 0
    
    # Evaluate every 4-cell window
    for window, coords in board.get_all_windows_with_coords():
        w = list(window)
        p1 = w.count(1)
        p2 = w.count(2)
        e  = w.count(0)

        # -------- Player 1 (AI) --------
        if p1 > 0 and p2 == 0:
            potential_bonus += p1

            if p1 == 3 and e == 1:
                i = w.index(0)
                r, c = coords[i]
                if is_playable(board, r, c):
                    winning_spots_p1.add((r, c))
                else:
                    floating_threes_p1 += 1

            elif p1 == 2 and e == 2:
                num_twos += 1

        # -------- Player 2 (Opponent) --------
        elif p2 > 0 and p1 == 0:
            potential_bonus -= p2

            if p2 == 3 and e == 1:
                i = w.index(0)
                r, c = coords[i]
                if is_playable(board, r, c):
                    winning_spots_p2.add((r, c))
                else:
                    floating_threes_p2 += 1

            elif p2 == 2 and e == 2:
                num_twos_opp += 1

    # Double-threat detection
    p1_double = int(len(winning_spots_p1) >= 2)
    p2_double = int(len(winning_spots_p2) >= 2)

    cnt = np.sum(board.table == 0)

    # Final weighted score
    score = (
        + 1e9 * p1_double
        + 1e5 * len(winning_spots_p1)
        + 100  * floating_threes_p1
        + 10   * num_twos
        + cnt  * potential_bonus
        
        - 10   * num_twos_opp
        - 100  * floating_threes_p2
        - 1e6 * len(winning_spots_p2)   # Immediate opponent threat
        - 1e9 * p2_double
    )

    return score


# ---------------- Alpha-Beta ----------------

'''
=====================================
alphabeta_strong
=====================================
Minimax search with alpha-beta pruning.

Features:
- Depth-limited search
- Move ordering favoring center columns
- Returns both best score and all equally optimal moves

This allows randomness without sacrificing optimality.
'''
def alphabeta_strong(board, depth, maximizingPlayer, alpha, beta, dep=4):
    valid_moves = board.get_valid_locations()
    is_terminal = board.terminate()
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.win(1): return 1e12, [-1]
            elif board.win(2): return -1e12, [-1]
            else: return 0, [-1]
        return get_heuristic_strong(board), valid_moves

    # Prefer center columns (standard Connect-4 strategy)
    center = board.column // 2
    valid_moves.sort(key=lambda x: abs(x - center))

    if maximizingPlayer:
        value = -np.inf
        best_moves = []
        for col in valid_moves:
            row = board.make_move(col, 1)
            score, _ = alphabeta_strong(board, depth-1, False, alpha, beta)
            board.undo_move(col, row)

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
        for col in valid_moves:
            row = board.make_move(col, 2)
            score, _ = alphabeta_strong(board, depth-1, True, alpha, beta)
            board.undo_move(col, row)

            if score < value:
                value = score
                best_moves = [col]
            elif score == value:
                best_moves.append(col)

            beta = min(beta, value)
            if alpha >= beta:
                break

        return value, best_moves


'''
=====================================
get_best_move
=====================================
Top-level decision function.

Steps:
1. Check for immediate win or forced defense
2. Otherwise, invoke alpha-beta search
3. Randomly choose among equally optimal moves
'''
def get_best_move(board_arr, player_piece, depth=4):
    board = Board(board_arr)

    # Forced immediate win / block
    for col in board.get_valid_locations():
        row = board.make_move(col, player_piece)
        if board.win(player_piece):
            board.undo_move(col, row)
            return col
        board.undo_move(col, row)

    score, moves = alphabeta_strong(
        board,
        depth,
        player_piece == 1,
        -np.inf,
        np.inf
    )

    return random.choice(moves) if moves else -1
