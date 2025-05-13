# Chess Game with GUI

A graphical user interface for a chess game with AI capabilities of varying difficulty levels.

## Features

- Visual chess board with proper piece representations
- Current player's turn indicator
- Game status display (check, checkmate, stalemate)
- Difficulty level selection for AI opponents
- Move history panel
- Captured pieces display
- Player scores

### User Interaction Features

- Click-to-select-and-move functionality
- Highlighting of valid moves when a piece is selected
- Visual indication of the last move made
- Option to restart the game or select a new difficulty
- Save/load game functionality
- Board flip option
- Option to play against another human player

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python installed
2. Install the required packages:
   ```
   pip install pygame
   ```
3. Run the asset creation script to generate chess piece images and sound files:
   ```
   python create_assets.py
   ```

## Usage

Run the chess GUI with:
```
python ChessGUI.py
```

### Controls

- Click on a piece to select it, then click on a destination square to move
- Use the buttons on the right panel to:
  - Start a new game
  - Change AI difficulty
  - Flip the board
  - Save/load game
  - Toggle between human vs. AI and human vs. human modes

### Keyboard Shortcuts

- N: Start a new game
- F: Flip the board
- S: Save game
- L: Load game

## Project Structure

- `ChessGUI.py`: Main GUI application
- `ChessGame.py`: Game logic and AI algorithms
- `ChessBoard.py`: Board representation and updating
- `Node.py`: Used for the minimax algorithm tree
- `create_assets.py`: Script to generate chess piece images and sound files
- `Chessnut/`: External library for chess rules and move validation

## Sound Credits

Sound effects are placeholders and can be replaced with your own sound files in the `sounds` directory.

## License

This project is open-source.
