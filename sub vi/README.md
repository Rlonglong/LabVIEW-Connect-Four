# Connect Four v0.0 – SubVI

## Overview
This project implements a basic version of **Connect Four** in LabVIEW.  
The game uses a 2D array to represent the board and provides SubVIs to handle game logic, moves, and board state.  
This README summarizes the included SubVIs and their functionalities.

---

## SubVIs

### 1. CheckMove.vi
- **Purpose:** Checks if a move is valid (whether a column is not full).  
- **Inputs:**  
  - `board` (2D array) – current game board  
  - `col` (I32) – target column  
- **Outputs:**  
  - `valid` (Boolean) – TRUE if the column has at least one empty slot  

### 2. PlacePiece.vi
- **Purpose:** Places a player's piece in the specified column.  
- **Inputs:**  
  - `board` (2D array) – current game board  
  - `col` (I32) – target column  
  - `player` (I32) – player ID  
- **Outputs:**  
  - `board_out` (2D array) – updated game board  

### 3. CheckWin.vi
- **Purpose:** Checks if a player has won by placing this col and connecting four pieces in any direction.  
- **Inputs:**  
  - `board` (2D array) – current game board  
  - `player` (I32) – player ID  
  - `col` (I32) - target column  
- **Outputs:**  
  - `win` (Boolean) – TRUE if the player has four in a row  
  - `winner` (I32) – returns the winning player ID if win = TRUE  

### 4. DrawBoard.vi
- **Purpose:** Draws the current state of the board on the 2D Picture Control.  
- **Inputs:**  
  - `board` (2D array) – current game board  
- **Outputs:**  
  - `UI` (2D Picture) - the UI to show  

### 5. DrawHover.vi
- **Purpose:** Shows a visual indicator (cross ✕) on columns that are full when the mouse hovers over them.  
- **Inputs:**  
  - `board` (2D array) – current game board  
  - `col` (I32) – hovered column  
  - `UI` (2D Picture) – current UI display  
- **Outputs:**  
  - `UI_out` (2D Picture) – updated UI with hover indicator  

### 6. GetValidMoves.vi
- **Purpose:** Returns the list of columns where a piece can still be placed.  
- **Inputs:**  
  - `board` (2D array) – current game board  
- **Outputs:**  
  - `validCols` (1D array of Boolean) – array of column indices that are valid moves  

### 7. IsBoardFull.vi
- **Purpose:** Checks if the board is full (tie condition).  
- **Inputs:**  
  - `board` (2D array) – current game board  
- **Outputs:**  
  - `full` (Boolean) – TRUE if no more moves are possible  

---

## Usage Notes
- Use `InitializeBoard.vi` at the start of a game to create an empty board.  
- For each player move:  
  1. Use `CheckMove.vi` to verify the column is valid.  
  2. Use `PlacePiece.vi` to update the board.  
  3. Use `CheckWin.vi` to check for a winning move.  
  4. Use `DrawBoard.vi` to update the UI.  
  5. Use `DrawHover.vi` to show cross indicators when hovering over full columns.  
- Use `GetValidMoves.vi` to get playable columns and `IsBoardFull.vi` to detect a draw.  

---

## File List
- `CheckMove.vi`  
- `CheckWin.vi`  
- `DrawBoard.vi`  
- `DrawHover.vi`  
- `GetValidMoves.vi`  
- `IsBoardFull.vi`  
- `PlacePiece.vi`  

---

## Version
- **Connect Four v1.2** – initial release, basic functionality only.