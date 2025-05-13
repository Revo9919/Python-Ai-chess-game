import pygame
import sys
import os
from pygame import mixer
from Chessnut import Game
from ChessBoard import ChessBoard
from ChessGame import select_ai_move, current_player

# Initialize pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_SIZE = SQUARE_SIZE - 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (124, 252, 0, 128)  # Semi-transparent green
MOVE_HIGHLIGHT = (255, 255, 0, 150)   # Semi-transparent yellow
LAST_MOVE_HIGHLIGHT = (135, 206, 250, 150)  # Semi-transparent light blue
TEXT_COLOR = (50, 50, 50)
PANEL_BG = (221, 221, 221)
BUTTON_COLOR = (120, 120, 120)
BUTTON_HOVER = (150, 150, 150)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

# Setup font
pygame.font.init()
font = pygame.font.SysFont('Arial', 16)
large_font = pygame.font.SysFont('Arial', 24)

# Load sounds
try:
    move_sound = mixer.Sound(os.path.join("sounds", "move.wav"))
    capture_sound = mixer.Sound(os.path.join("sounds", "capture.wav"))
    check_sound = mixer.Sound(os.path.join("sounds", "check.wav"))
    game_over_sound = mixer.Sound(os.path.join("sounds", "game_over.wav"))
except:
    print("Sound files not found. Creating sounds directory...")
    os.makedirs("sounds", exist_ok=True)
    # We'll continue without sounds

# Dictionary to store piece images
piece_images = {}

def create_piece_image(piece_code, size=PIECE_SIZE):
    """Create a simple image for a chess piece with its symbol"""
    piece_symbols = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
    piece_letters = {
        'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P',
        'k': 'k', 'q': 'q', 'r': 'r', 'b': 'b', 'n': 'n', 'p': 'p'
    }

    is_white_piece = piece_code.isupper()
    piece_color = WHITE if is_white_piece else BLACK
    bg_color = (210, 180, 140)  # Tan background

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))  # Transparent background

    circle_radius = size // 2 - 2
    pygame.draw.circle(surf, bg_color, (size // 2, size // 2), circle_radius)
    pygame.draw.circle(surf, BLACK if is_white_piece else WHITE, (size // 2, size // 2), circle_radius, 1)

    symbol_rendered_successfully = False
    symbol = piece_symbols.get(piece_code, '?')
    font_size_symbol = int(size * 0.7)
    # Added 'DejaVu Sans', 'FreeSerif' which have good Unicode coverage
    font_candidates = ['Arial Unicode MS', 'Segoe UI Symbol', 'DejaVu Sans', 'FreeSerif', 'Arial', 'Times New Roman']
    
    print(f"Attempting to render Unicode symbol for {piece_code} ('{symbol}')")
    for font_name in font_candidates:
        try:
            font = pygame.font.SysFont(font_name, font_size_symbol, bold=True)
            text_surface = font.render(symbol, True, piece_color)
            # Heuristic: width should be somewhat substantial, not tiny (like a missing char box)
            # and not wider than the available space.
            if size * 0.1 < text_surface.get_width() < size * 0.95:
                text_rect = text_surface.get_rect(center=(size // 2, size // 2))
                surf.blit(text_surface, text_rect)
                symbol_rendered_successfully = True
                print(f"  Successfully rendered Unicode symbol '{symbol}' for {piece_code} using font {font_name}")
                break 
        except Exception as e:
            print(f"  Font {font_name} failed for Unicode symbol '{symbol}' for {piece_code}: {e}")
            continue

    if symbol_rendered_successfully:
        return surf

    print(f"Falling back to letter for {piece_code}")
    letter = piece_letters.get(piece_code, '?')
    try:
        letter_font_size = int(size * 0.75) 
        letter_font = pygame.font.SysFont('Arial', letter_font_size, bold=True) # Arial is very common
        text_surface = letter_font.render(letter, True, piece_color)
        text_rect = text_surface.get_rect(center=(size // 2, size // 2))
        surf.blit(text_surface, text_rect)
        print(f"  Successfully rendered letter '{letter}' for {piece_code}")
        return surf
    except Exception as e:
        print(f"  Error rendering letter '{letter}' for {piece_code}: {e}")

    print(f"Falling back to piece_code character for {piece_code}")
    try:
        code_font_size = int(size * 0.6)
        code_font = pygame.font.SysFont('Arial', code_font_size, bold=True)
        text_surface = code_font.render(piece_code, True, piece_color)
        text_rect = text_surface.get_rect(center=(size // 2, size // 2))
        surf.blit(text_surface, text_rect)
        print(f"  Successfully rendered piece_code char '{piece_code}'")
    except Exception as e:
        print(f"  Error rendering piece_code char '{piece_code}': {e}")

    return surf

def load_piece_images():
    """Load chess piece images from 'pieces' directory or create them if missing"""
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    
    if not os.path.exists("pieces"):
        print("Creating pieces directory...")
        os.makedirs("pieces", exist_ok=True)
    
    missing_pieces = False
    
    for piece in pieces:
        img_path = os.path.join("pieces", f"{piece}.png")
        try:
            if os.path.exists(img_path):
                # Load existing image
                img = pygame.image.load(img_path)
                piece_images[piece] = pygame.transform.scale(img, (PIECE_SIZE, PIECE_SIZE))
            else:
                # Create image if it doesn't exist
                print(f"Creating image for piece: {piece}")
                img = create_piece_image(piece)
                piece_images[piece] = img
                # Save for future use
                pygame.image.save(img, img_path)
                missing_pieces = True
        except Exception as e:
            print(f"Error with piece {piece}: {e}")
            # Create a fallback image
            piece_images[piece] = create_piece_image(piece)
    
    if missing_pieces:
        print("Some piece images were automatically created. For better visuals, you may want to replace them with proper chess piece images.")
    
    return True

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                if self.action:
                    self.action()
                return True
        return False

class ChessGUI:
    def __init__(self):
        self.board_offset_x = 20
        self.board_offset_y = 20
        self.board = ChessBoard(8, 8)
        self.game = Game()
        self.board.updateBoard(str(self.game))
        
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        self.game_status = self.game.status
        self.difficulty = "2"  # Default medium difficulty
        self.move_history = []
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.scores = {"White": 0, "Black": 0}
        self.board_flipped = False
        self.game_over = False
        self.player_timers = {"White": 600, "Black": 600}  # 10 minutes per player
        self.timer_active = False
        self.current_time = 0
        self.timer_running = False
        self.human_vs_human = False
        self.notation_input = ""
        self.notation_active = False
        
        # Create buttons
        self.new_game_btn = Button(650, 50, 120, 30, "New Game", self.new_game)
        self.difficulty_btn = Button(650, 90, 120, 30, f"Difficulty: {self.difficulty}", self.change_difficulty)
        self.flip_board_btn = Button(650, 130, 120, 30, "Flip Board", self.flip_board)
        self.save_game_btn = Button(650, 170, 120, 30, "Save Game", self.save_game)
        self.load_game_btn = Button(650, 210, 120, 30, "Load Game", self.load_game)
        self.toggle_mode_btn = Button(650, 250, 120, 30, "vs Computer", self.toggle_game_mode)
        
        self.buttons = [self.new_game_btn, self.difficulty_btn, self.flip_board_btn, 
                       self.save_game_btn, self.load_game_btn, self.toggle_mode_btn]
    
    def new_game(self):
        """Start a new chess game"""
        self.game = Game()
        self.board.updateBoard(str(self.game))
        self.move_history = []
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        self.game_status = self.game.status
        self.game_over = False
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.player_timers = {"White": 600, "Black": 600}
        self.timer_running = False
    
    def change_difficulty(self):
        """Cycle through difficulty levels"""
        difficulties = {"1": "Easy", "2": "Medium", "3": "Hard"}
        next_diff = {"1": "2", "2": "3", "3": "1"}
        self.difficulty = next_diff[self.difficulty]
        self.difficulty_btn.text = f"Difficulty: {difficulties[self.difficulty]}"
    
    def flip_board(self):
        """Toggle board orientation"""
        self.board_flipped = not self.board_flipped
    
    def save_game(self):
        """Save the current game state"""
        try:
            with open("saved_game.txt", "w") as f:
                f.write(f"{self.game.get_fen()}\n")
                f.write(f"{self.difficulty}\n")
                f.write(f"{','.join(self.move_history)}\n")
                f.write(f"{self.player_timers['White']},{self.player_timers['Black']}\n")
                f.write(f"{int(self.human_vs_human)}\n")
            print("Game saved successfully")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self):
        """Load a saved game state"""
        try:
            if not os.path.exists("saved_game.txt"):
                print("No saved game found")
                return
                
            with open("saved_game.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 5:
                    fen = lines[0].strip()
                    self.difficulty = lines[1].strip()
                    self.difficulty_btn.text = f"Difficulty: {['Easy', 'Medium', 'Hard'][int(self.difficulty)-1]}"
                    
                    self.move_history = lines[2].strip().split(',') if lines[2].strip() else []
                    
                    times = lines[3].strip().split(',')
                    if len(times) == 2:
                        self.player_timers["White"] = float(times[0])
                        self.player_timers["Black"] = float(times[1])
                    
                    self.human_vs_human = bool(int(lines[4].strip()))
                    self.toggle_mode_btn.text = "vs Human" if self.human_vs_human else "vs Computer"
                    
                    self.game.set_fen(fen)
                    self.board.updateBoard(str(self.game))
                    self.game_status = self.game.status
                    self.update_captured_pieces()
                    self.selected_piece = None
                    self.selected_square = None
                    self.valid_moves = []
                    self.game_over = self.game_status in [2, 3]
                    
                    print("Game loaded successfully")
                else:
                    print("Invalid save file format")
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def toggle_game_mode(self):
        """Toggle between human vs computer and human vs human modes"""
        self.human_vs_human = not self.human_vs_human
        self.toggle_mode_btn.text = "vs Human" if self.human_vs_human else "vs Computer"
        self.new_game()
    
    def update_captured_pieces(self):
        """Update the lists of captured pieces based on what's missing from the board"""
        # This is a simplified implementation - you might want to track captures as they happen
        current_pieces = self.parse_board_state()
        all_pieces = {
            'P': 8, 'N': 2, 'B': 2, 'R': 2, 'Q': 1, 'K': 1,
            'p': 8, 'n': 2, 'b': 2, 'r': 2, 'q': 1, 'k': 1
        }
        
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        
        # Count current pieces
        current_count = {}
        for piece in all_pieces:
            current_count[piece] = current_pieces.count(piece)
        
        # Determine captured pieces
        for piece, count in all_pieces.items():
            diff = count - current_count[piece]
            if diff > 0:
                if piece.isupper():  # White piece was captured
                    self.captured_pieces_black.extend([piece] * diff)
                else:  # Black piece was captured
                    self.captured_pieces_white.extend([piece] * diff)
                    
        # Calculate scores based on piece values
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
                        'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
        
        self.scores["White"] = sum(piece_values[p] for p in self.captured_pieces_white)
        self.scores["Black"] = sum(piece_values[p] for p in self.captured_pieces_black)
    
    def parse_board_state(self):
        """Extract all pieces from the current board state"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board.data[row][col]
                if piece != ' ':
                    pieces.append(piece)
        return pieces
    
    def square_to_notation(self, row, col):
        """Convert board coordinates to algebraic notation (e.g., 0,0 -> a8)"""
        return chr(col + 97) + str(8 - row)
    
    def notation_to_square(self, notation):
        """Convert algebraic notation to board coordinates (e.g., a8 -> 0,0)"""
        if len(notation) != 2:
            return None
        col = ord(notation[0]) - 97
        row = 8 - int(notation[1])
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None
    
    def get_square_from_pos(self, pos):
        """Convert screen position to board coordinates"""
        x, y = pos
        if (x < self.board_offset_x or x >= self.board_offset_x + BOARD_SIZE or 
            y < self.board_offset_y or y >= self.board_offset_y + BOARD_SIZE):
            return None
        
        col = (x - self.board_offset_x) // SQUARE_SIZE
        row = (y - self.board_offset_y) // SQUARE_SIZE
        
        if self.board_flipped:
            col = 7 - col
            row = 7 - row
            
        return row, col
    
    def get_valid_moves_for_piece(self, row, col):
        """Get all valid moves for the piece at specified position"""
        square_notation = self.square_to_notation(row, col)
        valid_moves = []
        
        # Get all possible moves
        all_moves = self.game.get_moves()
        
        # Filter moves starting from our square
        for move in all_moves:
            if move.startswith(square_notation):
                valid_moves.append(move)
                
        return valid_moves
    
    def handle_click(self, pos):
        """Handle mouse clicks on the board"""
        if self.game_over:
            return
            
        square = self.get_square_from_pos(pos)
        if not square:
            return
            
        row, col = square
        
        # Get the current player
        current = 'w' if self.game.state[0] == 'w' else 'b'
        piece = self.board.data[row][col]
        
        # Enforce player turns in human vs human mode
        if self.human_vs_human:
            # White's turn and clicked on black piece or vice versa
            if (current == 'w' and piece.islower()) or (current == 'b' and piece.isupper()):
                return
                
        # Computer's turn in AI mode
        if not self.human_vs_human and current == 'b':
            return
            
        # If a piece is already selected
        if self.selected_piece:
            selected_row, selected_col = self.selected_piece
            from_notation = self.square_to_notation(selected_row, selected_col)
            to_notation = self.square_to_notation(row, col)
            move = from_notation + to_notation
            
            # Check if the move is in the valid moves list
            if move in self.valid_moves:
                self.make_move(move)
            else:
                # If clicked on another valid piece of the same color, select it instead
                if ((current == 'w' and piece.isupper()) or 
                    (current == 'b' and piece.islower())):
                    self.selected_piece = (row, col)
                    self.valid_moves = self.get_valid_moves_for_piece(row, col)
                else:
                    # Otherwise, deselect
                    self.selected_piece = None
                    self.valid_moves = []
        else:
            # Select a piece if it belongs to the current player
            if piece != ' ' and ((current == 'w' and piece.isupper()) or 
                                (current == 'b' and piece.islower())):
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves_for_piece(row, col)
    
    def make_move(self, move):
        """Apply a move to the game state"""
        # Check if move is valid
        if move in self.game.get_moves():
            # Check if a piece is being captured
            is_capture = False
            to_square = move[2:4]
            to_coords = self.notation_to_square(to_square)
            if to_coords:
                row, col = to_coords
                if self.board.data[row][col] != ' ':
                    is_capture = True
            
            # Apply the move
            self.game.apply_move(move)
            self.board.updateBoard(str(self.game))
            self.last_move = move
            self.move_history.append(move)
            
            # Update game status and captured pieces
            self.game_status = self.game.status
            self.update_captured_pieces()
            
            # Play appropriate sound
            try:
                if is_capture:
                    capture_sound.play()
                else:
                    move_sound.play()
            except:
                pass
            
            # Check for game over
            if self.game_status == 2:  # Checkmate
                self.game_over = True
                try:
                    game_over_sound.play()
                except:
                    pass
            elif self.game_status == 3:  # Stalemate
                self.game_over = True
                try:
                    game_over_sound.play()
                except:
                    pass
            elif self.game_status == 1:  # Check
                try:
                    check_sound.play()
                except:
                    pass
            
            # Reset selection
            self.selected_piece = None
            self.valid_moves = []
            
            # If playing against AI and it's AI's turn
            if not self.human_vs_human and not self.game_over and self.game.state[0] == 'b':
                self.make_ai_move()
    
    def make_ai_move(self):
        """Have the AI make a move"""
        ai_move = select_ai_move(self.difficulty)
        if ai_move:
            # Slight delay to make it seem like the AI is thinking
            pygame.time.delay(500)
            print(f"AI is making move: {ai_move}")
            self.make_move(ai_move)
        else:
            print("AI couldn't find a valid move")
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                # Determine color
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Apply flipping if needed
                draw_row, draw_col = row, col
                if self.board_flipped:
                    draw_row, draw_col = 7 - row, 7 - col
                
                # Draw square
                x = self.board_offset_x + draw_col * SQUARE_SIZE
                y = self.board_offset_y + draw_row * SQUARE_SIZE
                pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                  # Draw coordinate labels
                if draw_col == 0:  # Left edge - row numbers
                    label = str(8 - draw_row)
                    text = font.render(label, True, BLACK if color == LIGHT_SQUARE else WHITE)
                    screen.blit(text, (x + 2, y + 2))
                if draw_row == 7:  # Bottom edge - column letters
                    label = chr(97 + draw_col)
                    text = font.render(label, True, BLACK if color == LIGHT_SQUARE else WHITE)
                    screen.blit(text, (x + SQUARE_SIZE - 12, y + SQUARE_SIZE - 18))
                    
    def draw_pieces(self):
        """Draw the chess pieces"""
        for row in range(8):
            for col in range(8):
                piece = self.board.data[row][col]
                if piece != ' ':
                    draw_row, draw_col = row, col
                    if self.board_flipped:
                        draw_row, draw_col = 7 - row, 7 - col
                        
                    x = self.board_offset_x + draw_col * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                    y = self.board_offset_y + draw_row * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                      # If the piece is not in our image cache, create it on the fly
                    if piece not in piece_images:
                        piece_images[piece] = create_piece_image(piece)
                    
                    # Draw the piece
                    screen.blit(piece_images[piece], (x, y))
    
    def get_unicode_piece(self, piece):
        """Convert piece character to Unicode chess symbol"""
        symbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        return symbols.get(piece, '?')
    
    def draw_highlights(self):
        """Draw highlights for selected piece, valid moves and last move"""
        # Highlight the selected square
        if self.selected_piece:
            row, col = self.selected_piece
            draw_row, draw_col = row, col
            if self.board_flipped:
                draw_row, draw_col = 7 - row, 7 - col
                
            x = self.board_offset_x + draw_col * SQUARE_SIZE
            y = self.board_offset_y + draw_row * SQUARE_SIZE
            
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(HIGHLIGHT_COLOR)
            screen.blit(highlight, (x, y))
        
        # Highlight valid moves
        for move in self.valid_moves:
            to_square = move[2:4]
            to_coords = self.notation_to_square(to_square)
            if to_coords:
                row, col = to_coords
                draw_row, draw_col = row, col
                if self.board_flipped:
                    draw_row, draw_col = 7 - row, 7 - col
                    
                x = self.board_offset_x + draw_col * SQUARE_SIZE
                y = self.board_offset_y + draw_row * SQUARE_SIZE
                
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(MOVE_HIGHLIGHT)
                screen.blit(highlight, (x, y))
        
        # Highlight last move
        if self.last_move:
            from_square = self.last_move[0:2]
            to_square = self.last_move[2:4]
            
            from_coords = self.notation_to_square(from_square)
            to_coords = self.notation_to_square(to_square)
            
            if from_coords and to_coords:
                for coords in [from_coords, to_coords]:
                    row, col = coords
                    draw_row, draw_col = row, col
                    if self.board_flipped:
                        draw_row, draw_col = 7 - row, 7 - col
                        
                    x = self.board_offset_x + draw_col * SQUARE_SIZE
                    y = self.board_offset_y + draw_row * SQUARE_SIZE
                    
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(LAST_MOVE_HIGHLIGHT)
                    screen.blit(highlight, (x, y))
    
    def draw_side_panel(self):
        """Draw the side panel with game information and controls"""
        # Draw panel background
        pygame.draw.rect(screen, PANEL_BG, (BOARD_SIZE + 40, 0, SCREEN_WIDTH - BOARD_SIZE - 40, SCREEN_HEIGHT))
        
        # Current player and status
        player_text = f"Current Player: {current_player()}"
        status_text = "Game Status: "
        
        if self.game_status == 0:
            status_text += "Normal"
        elif self.game_status == 1:
            status_text += "CHECK"
        elif self.game_status == 2:
            status_text += "CHECKMATE"
        elif self.game_status == 3:
            status_text += "STALEMATE"
            
        player_surface = font.render(player_text, True, TEXT_COLOR)
        status_surface = font.render(status_text, True, TEXT_COLOR)
        
        screen.blit(player_surface, (BOARD_SIZE + 60, 20))
        screen.blit(status_surface, (BOARD_SIZE + 60, 40))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        
        # Display move history
        history_text = large_font.render("Move History:", True, TEXT_COLOR)
        screen.blit(history_text, (650, 300))
        
        if self.move_history:
            history_y = 330
            for i, move in enumerate(self.move_history[-10:]):  # Show last 10 moves
                if i % 2 == 0:  # White's move
                    move_text = f"{(i//2)+1}. {move}"
                else:  # Black's move
                    move_text = f"   {move}"
                move_surface = font.render(move_text, True, TEXT_COLOR)
                screen.blit(move_surface, (650, history_y + (i * 20)))
        
        # Display captured pieces
        white_captures_text = large_font.render("White Captures:", True, TEXT_COLOR)
        black_captures_text = large_font.render("Black Captures:", True, TEXT_COLOR)
        
        screen.blit(white_captures_text, (550, 500))
        screen.blit(black_captures_text, (700, 500))
        
        # Display the captured pieces
        for i, piece in enumerate(self.captured_pieces_white):
            x = 550 + (i % 6) * 20
            y = 530 + (i // 6) * 20
            if piece in piece_images:
                small_img = pygame.transform.scale(piece_images[piece], (20, 20))
                screen.blit(small_img, (x, y))
            else:
                piece_text = font.render(self.get_unicode_piece(piece), True, BLACK)
                screen.blit(piece_text, (x, y))
                
        for i, piece in enumerate(self.captured_pieces_black):
            x = 700 + (i % 6) * 20
            y = 530 + (i // 6) * 20
            if piece in piece_images:
                small_img = pygame.transform.scale(piece_images[piece], (20, 20))
                screen.blit(small_img, (x, y))
            else:
                piece_text = font.render(self.get_unicode_piece(piece), True, BLACK)
                screen.blit(piece_text, (x, y))
        
        # Display scores
        white_score_text = font.render(f"Score: {self.scores['White']}", True, TEXT_COLOR)
        black_score_text = font.render(f"Score: {self.scores['Black']}", True, TEXT_COLOR)
        
        screen.blit(white_score_text, (550, 580))
        screen.blit(black_score_text, (700, 580))
        
        # Display player timers
        white_timer = self.format_time(self.player_timers["White"])
        black_timer = self.format_time(self.player_timers["Black"])
        
        white_timer_text = font.render(f"Time: {white_timer}", True, TEXT_COLOR)
        black_timer_text = font.render(f"Time: {black_timer}", True, TEXT_COLOR)
        
        screen.blit(white_timer_text, (550, 600))
        screen.blit(black_timer_text, (700, 600))
    
    def format_time(self, seconds):
        """Format seconds to MM:SS"""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02}:{secs:02}"
    
    def update_timers(self, dt):
        """Update the player timers"""
        if not self.timer_running or self.game_over:
            return
            
        current = "White" if self.game.state[0] == 'w' else "Black"
        self.player_timers[current] -= dt
        
        # Check for time out
        if self.player_timers[current] <= 0:
            self.player_timers[current] = 0
            self.game_over = True
            print(f"{current} lost on time")
    
    def draw(self):
        """Draw the complete game interface"""
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the board and pieces
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        
        # Draw the side panel
        self.draw_side_panel()
        
        # Draw game over message if applicable
        if self.game_over:
            overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            screen.blit(overlay, (self.board_offset_x, self.board_offset_y))
            
            if self.game_status == 2:  # Checkmate
                winner = "Black" if self.game.state[0] == 'w' else "White"
                message = f"{winner} wins by checkmate!"
            elif self.game_status == 3:  # Stalemate
                message = "Draw by stalemate!"
            else:  # Time out
                current = "White" if self.game.state[0] == 'w' else "Black"
                opponent = "Black" if current == "White" else "White"
                if self.player_timers[current] <= 0:
                    message = f"{opponent} wins on time!"
                else:
                    message = "Game over!"
                    
            text = large_font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(self.board_offset_x + BOARD_SIZE//2, self.board_offset_y + BOARD_SIZE//2))
            screen.blit(text, text_rect)
            
            # Draw restart prompt
            restart_text = font.render("Press 'N' to start a new game", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.board_offset_x + BOARD_SIZE//2, self.board_offset_y + BOARD_SIZE//2 + 30))
            screen.blit(restart_text, restart_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0  # Convert to seconds
            self.update_timers(dt)
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Check for hover states on buttons
            for button in self.buttons:
                button.check_hover(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle key presses
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.new_game()
                    elif event.key == pygame.K_f:
                        self.flip_board()
                    elif event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()
                        
                # Handle mouse clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                    button_clicked = False
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos, event):
                            button_clicked = True
                            break
                    
                    # If no button was clicked, check board interaction
                    if not button_clicked:
                        self.handle_click(mouse_pos)
                        
            # Draw everything
            self.draw()
            
        pygame.quit()
        sys.exit()

def main():
    """Main function to start the chess GUI"""
    # Check and create directories for assets
    os.makedirs("sounds", exist_ok=True)
    os.makedirs("pieces", exist_ok=True)
    
    print("Loading and creating chess piece images...")
      # Create piece images with Unicode chess symbols
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    piece_symbols = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
    
    for piece in pieces:
        img_path = os.path.join("pieces", f"{piece}.png")
        
        # Try to load existing image first
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path)
                piece_images[piece] = pygame.transform.scale(img, (PIECE_SIZE, PIECE_SIZE))
                print(f"Loaded image for {piece}")
                continue
            except Exception as e:
                print(f"Error loading image for {piece}: {e}")
        
        # If loading fails or file doesn't exist, create a very simple image
        print(f"Creating simple image for {piece}")
        
        # Create a simple colored circle with letter
        is_white_piece = piece.isupper()
        piece_color = BLACK if is_white_piece else WHITE
        bg_color = WHITE if is_white_piece else BLACK
        
        # Create surface
        surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # Transparent background
        
        # Draw circle
        circle_radius = PIECE_SIZE // 2 - 2
        pygame.draw.circle(surf, bg_color, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius)
        pygame.draw.circle(surf, piece_color, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius, 2)
          # Draw Unicode chess symbol
        font_size = int(PIECE_SIZE * 0.7)
        # Try several fonts for better Unicode symbol support
        symbol = piece_symbols.get(piece, '?')
        symbol_rendered = False
        
        for font_name in ['Arial Unicode MS', 'Segoe UI Symbol', 'DejaVu Sans', 'FreeSerif', 'Arial']:
            try:
                symbol_font = pygame.font.SysFont(font_name, font_size, bold=True)
                text = symbol_font.render(symbol, True, piece_color)
                if text.get_width() > 5:  # Check if symbol rendered properly
                    text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
                    surf.blit(text, text_rect)
                    symbol_rendered = True
                    print(f"Successfully rendered {piece} with font {font_name}")
                    break
            except Exception as e:
                print(f"Failed to render {piece} with font {font_name}: {e}")
                continue
                
        # Fallback to letter if Unicode rendering failed
        if not symbol_rendered:
            print(f"Falling back to letter for {piece}")
            font_size = int(PIECE_SIZE * 0.6)
            letter_font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = letter_font.render(piece, True, piece_color)
            text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
            surf.blit(text, text_rect)
        
        # Save the piece image
        piece_images[piece] = surf
        try:
            pygame.image.save(surf, img_path)
        except Exception as e:
            print(f"Error saving image for {piece}: {e}")
    
    # Start the game
    gui = ChessGUI()
    gui.run()

if __name__ == "__main__":
    main()
