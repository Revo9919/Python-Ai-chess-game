from Chessnut import Game
from ChessBoard import *
import random
from Node import Node

# This program simulates a chess game with ChessNut library, integrating a GUI and an intelligent chess agent.

# Global variables
board = ChessBoard(8, 8)
chess_game = Game()  # New chess game instance
player_next_moves = {}  # Stores next two moves for the human player
ai_next_moves = {}  # Stores next two moves for the AI
board.updateBoard(str(chess_game))
# Piece values for scoring
piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 0}

# Scores for each player
white_score = 0
black_score = 0

# Checks and prints the game status like check, checkmate, or stalemate
def check_game_status():
    match chess_game.status:
        case 1:
            print("CHECK")
        case 2:
            print("CHECKMATE")
            print("GAME OVER")
        case 3:
            print("STALEMATE")

# Returns the current player ('White' or 'Black')
def current_player():
    return "White" if chess_game.state[0] == 'w' else "Black"

# Minimax algorithm for chess AI decision making
def minimax(node, depth, is_maximizing_player):
    if depth == 0 or node.leaf:
        heuristic_value = find_best_move('b')
        return heuristic_value

    if is_maximizing_player:
        best_value = -float('inf')
        for child in node.children:
            value = minimax(Node(child), depth - 1, False)
            best_value = max(best_value, value)
    else:
        best_value = float('inf')
        for child in node.children:
            value = minimax(Node(child), depth - 1, True)
            best_value = min(best_value, value)

    return best_value

# Heuristic to evaluate the best move based on piece values
def find_best_move(player):
    possible_moves = chess_game.get_moves(player)
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 200, ' ': 0}
    moves_score = {}

    for move in possible_moves:
        target_square = move[2:]
        piece = board.lookupPiece(target_square).lower()
        moves_score[move] = piece_values[piece]

    max_value = max(moves_score.values())
    best_moves = [move for move, value in moves_score.items() if value == max_value]
    return random.choice(best_moves)

# Generates potential future moves based on current board state
def predict_future_moves(player):
    future_moves = {}
    current_fen = chess_game.get_fen()

    for move in chess_game.get_moves(player):
        chess_game.apply_move(move)
        future_moves[move] = chess_game.get_moves(player)
        chess_game.set_fen(current_fen)

    return future_moves

# Selects an AI move based on difficulty chosen by user
def select_ai_move(difficulty):
    match difficulty:
        case "1":
            return random_move()
        case "2":
            return best_move()
        case "3":
            return minimax_move()

# Runs the chess game loop, handling user interactions and AI moves
def run_game():
    print("\nWelcome to Chess AI!")
    print('Player is white, AI is black')
    print('Instructions: Enter move in the format "e2e4" for moving a piece from e2 to e4.')

    difficulty = input("Choose AI difficulty (1: Easy, 2: Medium, 3: Hard): ")
    while difficulty not in ["1", "2", "3"]:
        difficulty = input("Invalid choice. Select 1, 2, or 3 for AI difficulty: ")

    while chess_game.status not in [2, 3]:  # Continue playing unless checkmate or stalemate
        print(f"\n{current_player()} to move.")
        move = input("Your move: ")
        if move in chess_game.get_moves('w'):
            chess_game.apply_move(move)
            board.updateBoard(str(chess_game))
            print("Board updated.")
            check_game_status()
            ai_move = select_ai_move(difficulty)
            chess_game.apply_move(ai_move)
            board.updateBoard(str(chess_game))
            print(f"AI moved {ai_move}.")
            check_game_status()
        else:
            print("Invalid move. Try again.")
# Heuristic function to evaluate the best move based on piece values
def find_best_move(player):
    possible_moves = chess_game.get_moves(player)
    piece_values = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 200, ' ': 0}
    moves_score = {}

    for move in possible_moves:
        target_square = move[2:]  # 'e4' from 'e2e4'
        piece = board.lookupPiece(target_square).lower()  # gets the piece at the target location
        moves_score[move] = piece_values[piece]  # assigns score based on piece value

    # Find the best moves by scoring
    max_value = max(moves_score.values(), default=0)  # Find max score, default to 0 if no moves
    best_moves = [move for move, value in moves_score.items() if value == max_value]
    return random.choice(best_moves) if best_moves else None  # Choose randomly among best moves

# Generates potential future moves for two layers deep (2-ply lookahead)
def predict_future_moves(player):
    future_moves = {}
    current_fen = chess_game.get_fen()

    # First layer of moves
    for move in chess_game.get_moves(player):
        chess_game.apply_move(move)
        # Second layer of moves based on the first move
        future_moves[move] = chess_game.get_moves(player)
        chess_game.set_fen(current_fen)  # Reset to original position

    return future_moves

# Selects an AI move based on the user-selected difficulty
def select_ai_move(difficulty):
    match difficulty:
        case "1":
            return random_move()
        case "2":
            return best_move()
        case "3":
            return minimax_move()

# Random move AI for easy difficulty
def random_move():
    possible_moves = chess_game.get_moves('b')
    return random.choice(possible_moves) if possible_moves else None

# Best move AI for medium difficulty
def best_move():
    return find_best_move('b')

# Minimax AI for hard difficulty
def minimax_move():
    root_node = Node(chess_game.get_fen())  # Create root node for current position
    return minimax(root_node, 2, True)  # Start minimax with depth 2 and maximizing true

# Main game loop to run the chess game
def run_game():
    print("\nWelcome to Chess AI!")
    print('Player is white (capital letters), AI is black (lowercase letters)')
    print('Instructions: Enter moves in standard chess notation (e.g., "e2 to e4").')

    difficulty = input("Choose AI difficulty (1: Easy, 2: Medium, 3: Hard): ")
    while difficulty not in ["1", "2", "3"]:
        difficulty = input("Invalid choice. Please enter 1, 2, or 3 for AI difficulty: ")
    while chess_game.status not in [2, 3]:  # Game continues unless there's checkmate or stalemate
        print(board)
        print(f"\n{current_player()} to move.")
        move = input("Your move: ")
        if move in chess_game.get_moves('w'):
            chess_game.apply_move(move)
            board.updateBoard(str(chess_game))
            print("Board updated.")
            check_game_status()
            ai_move = select_ai_move(difficulty)
            chess_game.apply_move(ai_move)
            board.updateBoard(str(chess_game))
            print(f"AI moved: {ai_move}.")
            check_game_status()
            print(board)
        else:
            print("Invalid move. Please try again.")
            print(f"Valid moves are: {chess_game.get_moves('w')}")


# Only run the game if this file is executed directly
if __name__ == "__main__":
    # Launch the GUI version instead of the console version
    import os
    import sys
    import subprocess
    print("Launching Chess GUI...")
    try:
        # Use the start_chess.py script which has proper error handling
        subprocess.run([sys.executable, "start_chess.py"])
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Falling back to text-based version...")
        run_game()