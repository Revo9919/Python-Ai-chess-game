import pygame
import os
import sys
import urllib.request
import time

# Initialize pygame
pygame.init()

# Constants
PIECE_SIZE = 64

# URLs for chess piece images - using Wikimedia Commons which has standard chess piece SVGs
# We'll use PNG versions for simplicity
PIECE_URLS = {
    'K': "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg",
    'Q': "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg",
    'R': "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg",
    'B': "https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg",
    'N': "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg",
    'P': "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg",
    'k': "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg",
    'q': "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg",
    'r': "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg",
    'b': "https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg",
    'n': "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg",
    'p': "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg"
}

# Alternative: use simple letters with clear color coding
def create_simple_letter_pieces():
    """Create simple letter-based chess pieces with clear colors"""
    print("Creating chess piece images with colored letters...")
    
    if not os.path.exists("pieces"):
        os.makedirs("pieces")
    
    pieces = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
    
    for piece in pieces:
        print(f"Creating image for {piece}...")
        
        is_white_piece = piece.isupper()
        piece_color = (0, 0, 0) if is_white_piece else (255, 255, 255)  # Black text for white pieces, white for black
        bg_color = (255, 255, 255) if is_white_piece else (0, 0, 0)      # White bg for white pieces, black for black
        
        # Create surface
        surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE))
        surf.fill(bg_color)
        
        # Draw border
        pygame.draw.rect(surf, (128, 128, 128), (0, 0, PIECE_SIZE, PIECE_SIZE), 2)
        
        # Draw letter
        font = pygame.font.SysFont('Arial', int(PIECE_SIZE * 0.8), bold=True)
        text_surf = font.render(piece, True, piece_color)
        text_rect = text_surf.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
        surf.blit(text_surf, text_rect)
        
        # Save the image
        file_path = os.path.join("pieces", f"{piece}.png")
        pygame.image.save(surf, file_path)
        print(f"  Saved to {file_path}")
    
    print("All piece images created successfully!")

if __name__ == "__main__":
    create_simple_letter_pieces()
