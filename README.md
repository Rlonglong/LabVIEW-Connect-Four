# LabVIEW Connect Four Project Documentation

## 1. Project Planning

### 1.1 Design Motivation
All team members enjoy board games, so this project focuses on the classic game Connect Four. The goal is to implement an interactive game board in LabVIEW, supporting both single-player (against AI) and two-player modes. This project allows practice with LabVIEW's graphical programming workflow, event handling, and logic evaluation. The system also plans to integrate AI (Alpha-Beta / Minimax) and machine learning techniques to create a computer opponent that can "learn or improve evaluation functions."

### 1.2 Requirement Analysis
The system must include the following features:

#### Basic Game Features
- Display a 7×6 Connect Four board
- Players can select a column using the mouse to place a piece
- Full columns cannot accept additional pieces
- Visual or audio feedback for illegal moves
- Automatic detection of a four-in-a-row
- Single-player mode (Player vs AI) and two-player mode
- Optional: countdown timer for AI or player moves
- Optional: online multiplayer

#### Interface and Display
- Use a 2D Picture Control to render the board
- Show the current player
- Preview the position when hovering the mouse over a column
- Update the board after each move
- Show a game-over screen when four-in-a-row occurs
- Optional: confirmation prompt after a move

#### Game Modes
- Computer can play automatically in single-player mode
- Difficulty adjustment available
- Switch between Player vs Computer and Player vs Player

### 1.3 Programming Workflow
1. Initialize board data (2D array)
2. Player actions:
   - Mouse hover → show preview
   - Click → validate column and place piece
3. Update board display and backend 2D array
4. Check win conditions
5. If AI mode → computer makes a move; otherwise wait for Player 2
6. Repeat until a win or draw

---

## 2. Player Instructions

### 2.1 Gameplay
Connect Four is a turn-based game where players drop pieces into columns. Pieces fall to the lowest available row. The first player to connect four of their pieces wins.

- Player 1: Red  
- Player 2 (or AI): Yellow  

Optional modes:
- Single-player (Player vs AI)  
- Local two-player (Player 1 vs Player 2)  
- Online two-player (Player 1 vs Player 2)  

### 2.2 Controls
- Select a valid column on your turn
- Wait for the opponent on their turn
- Cannot place a piece in a full column
- The system automatically switches turns and updates the board
- Game ends when a player wins, with option to return to main menu

### 2.3 Scoring and Win Conditions
- A player wins by connecting four pieces in any direction:
  - Horizontal
  - Vertical
  - Main diagonal (↘)
  - Anti-diagonal (↗)
- If the board is full without four-in-a-row → draw

### 2.4 Game Flow
1. Select game mode  
2. Enter the board interface  
3. Players take turns  
4. System checks for four-in-a-row  
5. End game → display result with option to restart

---

## 3. AI Player Documentation

This section describes the design, planned integration, model architecture, and game logic of the AI player. The AI aims to provide adjustable difficulty, strategic gameplay, and future expandability for learning. See the implement at [AI Agent](./AI%20agent/)

### 3.1 Design Principles
1. **Adjustable Difficulty**  
AI strength can be tuned via:
   - Search depth  
   - Evaluation function complexity  
   - Alpha-Beta pruning on/off  

2. **Modular and Integrable**  
The AI functions as an independent module, receiving:
   - Current board (2D array)  
   - Current player  

Returns:
   - Recommended move column index  

This allows LabVIEW to switch easily between AI and Player 2 without modifying the main interface, and supports future AI extensions.

3. **Performance and Complexity**  
Alpha-Beta pruning ensures the AI operates efficiently, balancing speed and strategy within the LabVIEW environment.

### 3.2 Integration Plan
The AI consists of two parts: decision engine and evaluation function.

#### 1. Minimax Search
- MAX: AI tries to maximize advantage  
- MIN: Assumes opponent minimizes AI’s advantage  
- Selects the column with the highest score  

Basic Flow:
1. Get current board state (2D array)  
2. Simulate all legal moves  
3. Recursively search next possible moves  
4. Evaluate leaf nodes  
5. Backpropagate scores via MIN/MAX  
6. Choose the best column

#### 2. Alpha-Beta Pruning
- `alpha` = best MAX value known  
- `beta` = best MIN value known  
- If `beta <= alpha`, prune branch to save computation

#### 3. Evaluation Function
When no win exists, the AI evaluates board advantage. The evaluation function `get_heuristic_strong()` includes:

1. **Potential Connections**  
- Score positions based on possible 2-, 3-, or 4-in-a-row in all directions  
- Consider blocked positions and future extension possibilities  
- AI prioritizes positions with high potential

2. **Dual Threat Score**  
- Reward positions creating two simultaneous threats  
- Penalize positions allowing opponent dual-threats  
- Allows AI to implement advanced tactics even with limited search depth

3. **Three-in-a-Row Adjustment**  
- Unstable three-in-a-row with blocked ends scored lower  
- Prevents AI from blindly pursuing weak positions

### 3.3 Integration with LabVIEW
- The AI acts as a submodule:
  - Receives 2D array board state from LabVIEW  
  - LabVIEW calls DLL / VI subroutine  
  - Returns recommended column index  
- Main loop applies the move, updates display, and checks for win
