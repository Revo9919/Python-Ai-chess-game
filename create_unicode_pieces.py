import pygame
import os
import sys

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
PIECE_SIZE = 64  # Larger size for better clarity

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)  # Light square color
DARK_BROWN = (181, 136, 99)    # Dark square color

def create_piece_images():
    """Create chess piece images with Unicode symbols"""
    print("Creating chess piece images with Unicode symbols...")
    
    if not os.path.exists("pieces"):
        os.makedirs("pieces")
    
    # Define pieces and Unicode symbols
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    piece_symbols = {
        'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
        'k': '\u265A', 'q': '\u265B', 'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
    }
    
    # Delete any existing piece images
    for piece in pieces:
        file_path = os.path.join("pieces", f"{piece}.png")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted existing image: {file_path}")
    
    # Try different fonts that might have good Unicode support
    font_candidates = [
        'Arial Unicode MS', 
        'Segoe UI Symbol', 
        'DejaVu Sans', 
        'FreeSerif', 
        'Noto Sans Symbols',
        'Times New Roman',
        'Arial'
    ]
    
    # For testing all fonts
    available_fonts = pygame.font.get_fonts()
    print(f"Available fonts: {len(available_fonts)}")
    for i, font in enumerate(available_fonts[:5]):  # Print first 5 fonts for info
        print(f"  {i+1}. {font}")
    
    for piece in pieces:
        print(f"\nCreating image for {piece}...")
        
        is_white_piece = piece.isupper()
        piece_color = BLACK if is_white_piece else WHITE
        bg_color = LIGHT_BROWN  # We'll use the same background for all pieces
        
        # Create surface with transparency
        surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # Transparent background
        
        # Draw a colored circle as background
        circle_radius = PIECE_SIZE // 2 - 4
        pygame.draw.circle(surf, bg_color, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius)
        pygame.draw.circle(surf, BLACK if is_white_piece else WHITE, (PIECE_SIZE // 2, PIECE_SIZE // 2), circle_radius, 2)
        
        # Get the Unicode symbol
        symbol = piece_symbols.get(piece, '?')
        symbol_rendered = False
        
        # Try with larger font size for better rendering
        font_size = int(PIECE_SIZE * 0.75)
        
        # Try to render with different fonts
        for font_name in font_candidates:
            try:
                print(f"  Trying font: {font_name}")
                font = pygame.font.SysFont(font_name, font_size, bold=True)
                text_surf = font.render(symbol, True, piece_color)
                
                # If the width is reasonable, consider it a good rendering
                width_ratio = text_surf.get_width() / PIECE_SIZE
                if 0.1 < width_ratio < 0.9:  # Should take up between 10% and 90% of the space
                    text_rect = text_surf.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
                    surf.blit(text_surf, text_rect)
                    symbol_rendered = True
                    print(f"  ✓ Successfully rendered with font {font_name}!")
                    break
                else:
                    print(f"  × Rendered width looks wrong with {font_name} (ratio: {width_ratio:.2f})")
            except Exception as e:
                print(f"  × Error with font {font_name}: {e}")
        
        # Fallback to a simple letter if Unicode rendering failed
        if not symbol_rendered:
            print(f"  ! Falling back to letter for {piece}")
            font_size = int(PIECE_SIZE * 0.6)
            letter_font = pygame.font.SysFont('Arial', font_size, bold=True)
            text_surf = letter_font.render(piece, True, piece_color)
            text_rect = text_surf.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
            surf.blit(text_surf, text_rect)
        
        # Save the image
        file_path = os.path.join("pieces", f"{piece}.png")
        pygame.image.save(surf, file_path)
        print(f"  Saved to {file_path}")
    
    print("\nAll piece images created successfully!")

if __name__ == "__main__":
    create_piece_images()
