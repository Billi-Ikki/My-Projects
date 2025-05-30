# Chess Game with AI

## Overview
A Python chess game where a human (White) plays an AI (Black) using Minimax with alpha-beta pruning, featuring a Tkinter GUI.

## Features
- Tkinter GUI with beige (`#B58863`) and blue (`#5D8AA8`) board.
- Supports castling, en passant, and pawn promotion.
- Human moves via clicks or algebraic notation (e.g., "e2e4").
- AI evaluates material, position, and king safety.

## How It Works
- Human moves White pieces via clicks or notation.
- AI (Black) responds using Minimax (depth=3).
- Tracks check, checkmate, stalemate, and scores.

## Requirements
- Python 3.7+
- Tkinter (included with Python)

Verify Tkinter:
```bash
python -c "import tkinter"
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Billi-Ikki/Projects.git
   ```
2. Navigate to Chess directory:
   ```bash
   cd Projects/Chess
   ```

## Usage
1. Run the game:
   ```bash
   python chess.py
   ```
2. Click to move White pieces; select promotion piece via dialog.
3. AI moves for Black automatically.
4. Click "New Game" to reset.
5. Game ends with checkmate/stalemate notification.

## Notes
- Adjust AI depth in `AIPlayer` for stronger play.
- Colors optimized for visibility.
- For personal use only.
