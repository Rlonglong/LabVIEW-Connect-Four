# LabVIEW Connect Four Project Documentation

## 0. Prerequisites & Setup

Before running this project, please complete the following steps:

1. **Install Python 3.12**
   - Python must be installed in its native installation path
   - Do not rely only on environment variables

2. **Install required Python package**
```bash
pip install numpy
```

---

## 1. Project Overview

### 1.1 Design Motivation
This project implements the classic board game **Connect Four** using LabVIEW. The purpose is to practice graphical programming, event handling, and user interface design while integrating a simple AI opponent.

Currently, the project supports:
- Local two-player mode
- Single-player mode against AI

### 1.2 Implemented Features

#### Game Modes
- **Player Mode**: Local two-player (Player vs Player)
- **AI Mode**: Player vs Computer

> Only the above two modes are implemented in this version.

#### User Interface Features
- 7×6 Connect Four board rendered using 2D Picture Control
- **Start Page** with two selectable modes: Player Mode and AI Mode
- Hover animation on start page:
  - Underline expands from center when hovering
  - Underline shrinks back faster when mouse leaves
- Board hover preview:
  - Highlights the column under the cursor
- Full column indicator:
  - If a column is full, hovering shows a cross (✕) above the column
- Automatic turn switching
- Automatic win detection

---

## 2. Gameplay Instructions

### 2.1 Basic Rules
Connect Four is a turn-based game where players drop pieces into columns. Pieces fall to the lowest available row.

- Player 1: Red
- Player 2 / AI: Yellow

The first player to connect four pieces wins.

### 2.2 Controls
- Hover over a column to preview placement
- Click to place a piece in a valid column
- Cannot place a piece in a full column
- Turns switch automatically

### 2.3 Win Conditions
- Connect four pieces horizontally, vertically, or diagonally
- If the board is full without a four-in-a-row, the game is a draw
