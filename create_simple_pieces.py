import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Constants
PIECE_SIZE = 54  # Size of each piece image

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_WHITE = (235, 235, 235)
BG_BLACK = (50, 50, 50)

def create_simple_piece_image(piece_code):
    """Create a very simple image for a chess piece with just a letter"""
    piece_letters = {
        'P': 'P', 'N': 'N', 'B': 'B', 'R': 'R', 'Q': 'Q', 'K': 'K',
        'p': 'p', 'n': 'n', 'b': 'b', 'r': 'r', 'q': 'q', 'k': 'k'
    }
    
    is_white_piece = piece_code.isupper()
    piece_color = BLACK if is_white_piece else WHITE
    bg_color = BG_WHITE if is_white_piece else BG_BLACK
    
    # Create surface
    surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))  # Transparent background
    
    # Draw circle
    circle_radius = PIECE_SIZE // 2 - 2
    pygame.draw.circle(surf, bg_color, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius)
    pygame.draw.circle(surf, piece_color, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius, 2)
    
    # Draw letter
    letter = piece_letters[piece_code]
    font_size = int(PIECE_SIZE * 0.6)
    try:
        letter_font = pygame.font.SysFont('Arial', font_size, bold=True)
        text = letter_font.render(letter, True, piece_color)
        text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
        surf.blit(text, text_rect)
    except Exception as e:
        print(f"Error rendering letter for {piece_code}: {e}")
    
    return surf

def main():
    # Ensure pieces directory exists
    if not os.path.exists("pieces"):
        os.makedirs("pieces", exist_ok=True)
    
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    
    for piece in pieces:
        print(f"Creating image for {piece}...")
        img_path = os.path.join("pieces", f"{piece}.png")
        
        # Create the piece image
        surf = create_simple_piece_image(piece)
        
        # Save the image
        try:
            pygame.image.save(surf, img_path)
            print(f"  Saved to {img_path}")
        except Exception as e:
            print(f"  Error saving image for {piece}: {e}")
    
    print("All piece images created successfully.")

if __name__ == "__main__":
    main()
    pygame.quit()
