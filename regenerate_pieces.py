import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Constants for piece size
PIECE_SIZE = 54  # Same as in ChessGUI.py

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def create_piece_images():
    """Create chess piece images with Unicode symbols"""
    print("Creating piece images with Unicode symbols...")
    
    # Create pieces directory if it doesn't exist
    if not os.path.exists("pieces"):
        os.makedirs("pieces", exist_ok=True)
    
    # Define pieces and their Unicode symbols
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    piece_symbols = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
    
    for piece in pieces:
        print(f"Creating image for {piece}...")
        img_path = os.path.join("pieces", f"{piece}.png")
        
        # Create a simple colored circle with Unicode symbol
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
        symbol = piece_symbols.get(piece, '?')
        symbol_rendered = False
        
        for font_name in ['Arial Unicode MS', 'Segoe UI Symbol', 'DejaVu Sans', 'FreeSerif', 'Arial', 'Times New Roman']:
            try:
                symbol_font = pygame.font.SysFont(font_name, font_size, bold=True)
                text = symbol_font.render(symbol, True, piece_color)
                if text.get_width() > 5:  # Check if symbol rendered properly
                    text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
                    surf.blit(text, text_rect)
                    symbol_rendered = True
                    break
            except Exception as e:
                continue
        
        # Fallback to letter if Unicode rendering failed
        if not symbol_rendered:
            letter_font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = letter_font.render(piece, True, piece_color)
            text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
            surf.blit(text, text_rect)
        
        # Save the piece image
        try:
            pygame.image.save(surf, img_path)
            print(f"  Saved to {img_path}")
        except Exception as e:
            print(f"  Error saving image: {e}")
    
    print("All piece images created successfully.")

if __name__ == "__main__":
    # Remove existing piece images first
    for piece in ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']:
        img_path = os.path.join("pieces", f"{piece}.png")
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
            except:
                pass
    
    # Create new piece images
    create_piece_images()
