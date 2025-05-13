import pygame
import os
import sys

# Initialize pygame
pygame.init()

# Constants
PIECE_SIZE = 64  # Larger size for better clarity

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)  # Light square color
DARK_BROWN = (181, 136, 99)    # Dark square color

def draw_king(surface, color, is_white):
    """Draw a king piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Cross on top
    line_width = 4 if is_white else 3
    top_y = center_y - PIECE_SIZE // 3
    pygame.draw.line(surface, WHITE if is_white else BLACK, 
                    (center_x, top_y - 8), 
                    (center_x, top_y + 8), line_width)
    pygame.draw.line(surface, WHITE if is_white else BLACK, 
                    (center_x - 8, top_y), 
                    (center_x + 8, top_y), line_width)
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def draw_queen(surface, color, is_white):
    """Draw a queen piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Crown points
    points = []
    radius = PIECE_SIZE // 3
    for i in range(5):  # 5-point crown
        angle = i * 72 - 90  # Start at the top, go clockwise
        x = center_x + int(radius * pygame.math.Vector2().from_polar((1, angle))[0])
        y = center_y + int(radius * pygame.math.Vector2().from_polar((1, angle))[1])
        
        # Draw small circle at each point
        small_radius = 3
        pygame.draw.circle(surface, WHITE if is_white else BLACK, (x, y), small_radius)
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def draw_rook(surface, color, is_white):
    """Draw a rook piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Castle top
    rect_width = PIECE_SIZE // 3
    rect_height = PIECE_SIZE // 5
    rect_x = center_x - rect_width // 2
    rect_y = center_y - PIECE_SIZE // 3
    pygame.draw.rect(surface, WHITE if is_white else BLACK, 
                    (rect_x, rect_y, rect_width, rect_height))
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def draw_bishop(surface, color, is_white):
    """Draw a bishop piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Bishop's hat (mitre)
    top_y = center_y - PIECE_SIZE // 4
    
    # Draw a triangle for the hat
    points = [
        (center_x, center_y - PIECE_SIZE // 3),  # Top
        (center_x - PIECE_SIZE // 6, center_y),  # Bottom left
        (center_x + PIECE_SIZE // 6, center_y),  # Bottom right
    ]
    pygame.draw.polygon(surface, WHITE if is_white else BLACK, points)
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def draw_knight(surface, color, is_white):
    """Draw a knight piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Knight's head (like an L shape)
    head_color = WHITE if is_white else BLACK
    points = [
        (center_x, center_y - PIECE_SIZE // 6),  # Middle
        (center_x - PIECE_SIZE // 6, center_y - PIECE_SIZE // 4),  # Left top
        (center_x + PIECE_SIZE // 6, center_y - PIECE_SIZE // 3),  # Right top
    ]
    pygame.draw.polygon(surface, head_color, points)
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def draw_pawn(surface, color, is_white):
    """Draw a pawn piece"""
    # Base
    center_x, center_y = PIECE_SIZE // 2, PIECE_SIZE // 2
    pygame.draw.circle(surface, color, (center_x, center_y), PIECE_SIZE // 2 - 5)
    
    # Pawn's head
    head_radius = PIECE_SIZE // 6
    pygame.draw.circle(surface, WHITE if is_white else BLACK, 
                      (center_x, center_y - PIECE_SIZE // 8), head_radius)
    
    # Draw outline
    pygame.draw.circle(surface, BLACK if is_white else WHITE, 
                      (center_x, center_y), PIECE_SIZE // 2 - 5, 2)

def create_shaped_piece_images():
    """Create chess piece images with distinctive shapes"""
    print("Creating chess piece images with distinctive shapes...")
    
    # Ensure pieces directory exists
    if not os.path.exists("pieces"):
        os.makedirs("pieces")
    
    # Define pieces
    pieces = {
        'K': (draw_king, WHITE, True),
        'Q': (draw_queen, WHITE, True),
        'R': (draw_rook, WHITE, True),
        'B': (draw_bishop, WHITE, True),
        'N': (draw_knight, WHITE, True),
        'P': (draw_pawn, WHITE, True),
        'k': (draw_king, BLACK, False),
        'q': (draw_queen, BLACK, False),
        'r': (draw_rook, BLACK, False),
        'b': (draw_bishop, BLACK, False),
        'n': (draw_knight, BLACK, False),
        'p': (draw_pawn, BLACK, False),
    }
    
    # Create each piece image
    for piece, (draw_func, color, is_white) in pieces.items():
        print(f"Creating image for {piece}...")
        
        # Create surface with transparency
        surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # Transparent background
        
        # Draw the piece using its specific function
        draw_func(surf, color, is_white)
        
        # Save the image
        file_path = os.path.join("pieces", f"{piece}.png")
        pygame.image.save(surf, file_path)
        print(f"  Saved to {file_path}")
    
    print("\nAll piece images created successfully!")

if __name__ == "__main__":
    create_shaped_piece_images()
