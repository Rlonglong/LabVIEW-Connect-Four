# Connect Four AI Agents

This repository contains AI agents for **Connect Four**, implemented to explore different search strategies and heuristic evaluations. The agents are designed to make optimal decisions based on game state evaluation, ranging from basic Minimax to advanced heuristics with Alpha-Beta pruning.

---

## Agents Overview

### 1. Minimax Agent
- **Strategy:** Recursively explores all possible moves up to a fixed depth.
- **Player Roles:** Alternates between maximizing and minimizing players.
- **Evaluation:** Uses a heuristic function (`get_heuristic`) to assign scores when reaching the depth limit or terminal states.
- **Goal:** Selects moves that maximize chances of winning while assuming the opponent plays optimally.

### 2. Alpha-Beta Agent
- **Strategy:** Optimized version of Minimax with **Alpha-Beta pruning**.
- **Efficiency:** Reduces unnecessary node expansions, allowing deeper search within the same computational budget.
- **Pruning Logic:**
  - α (alpha): Best guaranteed score for the maximizing player.
  - β (beta): Best guaranteed score for the minimizing player.
  - Branches are pruned when they cannot influence the final decision.
- **Goal:** Maintain optimal move selection with improved performance compared to standard Minimax.

### 3. Strong AI Agent (`agent_strong`)
- **Strategy:** Uses an advanced heuristic evaluation function (`get_heuristic_strong`) to prioritize moves based on potential connections and winning threats.
- **Heuristic Components:**
  - **Potential bonus:** Evaluates possible link opportunities for each piece.
  - **For-win bonus:** Rewards dual-threat positions and immediate winning opportunities.
  - **Three bonus:** Detects near-winning combinations and adjusts weighting dynamically.
- **Goal:** Go beyond Alpha-Beta by choosing positions with higher potential for long-term success and attacking opportunities.

---

## Heuristic Highlights

The `get_heuristic_strong` function considers:

- **Immediate Wins/Losses:** Assigns large positive/negative scores if a win or loss is detected.
- **Two-in-a-row Patterns:** Rewards the AI for building potential lines while penalizing opponent two-in-a-row sequences.
- **Three-in-a-row Patterns:** 
  - Rewards meaningful three-in-a-row sequences that contribute toward winning.
  - **Ignores or penalizes isolated/insignificant threes** to avoid overvaluing accidental patterns.
- **Four-in-a-row Opportunities (non-winning):**
  - Detects potential four-piece sequences that could become threats.
  - **Deducts points for ineffective or blocked four-in-a-row patterns**, balancing offensive and defensive evaluation.
- **Potential Connections:** Evaluates open spaces around existing pieces to estimate future opportunities.
- **Dynamic Scoring:** Adjusts weights as the game progresses to favor offensive or defensive moves depending on board state.

This heuristic ensures the AI:
- Favors moves that increase the agent’s potential to win.
- Devalues insignificant patterns that do not contribute meaningfully.
- Penalizes opponent threats proportionally to their immediacy.
- Balances offensive and defensive strategies to achieve higher win rates against standard Alpha-Beta agents.

---

## Usage

1. Provide the current board state and specify which player the AI controls.
2. Call the desired agent function (`minimax`, `alphabeta`, `agent_strong`) with the board and depth limit (if applicable).
3. The agent returns the **selected move** (column index) to play.

```python
move = agent_strong(board, player_id)
