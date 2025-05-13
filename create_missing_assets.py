import pygame
import os
import sys

"""
Quick script to create all chess piece images.
This will create both white and black piece images.
"""

# Initialize pygame
pygame.init()
pygame.font.init()

# Create piece directories
os.makedirs("pieces", exist_ok=True)
os.makedirs("sounds", exist_ok=True)

# Define colors and sizes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (210, 180, 140)  # Light tan background
SIZE = 64  # Standard piece size
FONT_SIZE = int(SIZE * 0.75)

# Define all pieces
pieces = {
    # White pieces (uppercase)
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    # Black pieces (lowercase)
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

print("Creating chess piece images...")

# Font for piece symbols
font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)

# Create each piece
for piece, symbol in pieces.items():
    filename = os.path.join("pieces", f"{piece}.png")
    
    # Skip if file exists
    if os.path.exists(filename):
        print(f"Piece {piece} already exists - skipping")
        continue
    
    # Determine color based on case
    is_white_piece = piece.isupper()
    color = WHITE if is_white_piece else BLACK
    
    # Create surface with transparency
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Transparent
    
    # Draw background circle
    circle_radius = SIZE // 2 - 4
    pygame.draw.circle(surface, BACKGROUND, (SIZE // 2, SIZE // 2), circle_radius)
    
    # Render the piece symbol
    text = font.render(symbol, True, color)
    text_rect = text.get_rect(center=(SIZE // 2, SIZE // 2))
    surface.blit(text, text_rect)
    
    # Save the image
    pygame.image.save(surface, filename)
    print(f"Created {piece}.png")

print("\nCreating sound files...")
# Create simple sound files if needed
sound_files = ["move.wav", "capture.wav", "check.wav", "game_over.wav"]

for sound in sound_files:
    sound_path = os.path.join("sounds", sound)
    if os.path.exists(sound_path):
        print(f"Sound {sound} already exists - skipping")
        continue
        
    # Create a minimal WAV file
    with open(sound_path, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write((36).to_bytes(4, 'little'))  # File size - 8
        f.write(b'WAVE')
        # Format chunk
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))  # Chunk size
        f.write((1).to_bytes(2, 'little'))   # Format: PCM (1)
        f.write((1).to_bytes(2, 'little'))   # Channels: Mono (1)
        f.write((22050).to_bytes(4, 'little'))  # Sample rate
        f.write((22050).to_bytes(4, 'little'))  # Byte rate
        f.write((1).to_bytes(2, 'little'))   # Block align
        f.write((8).to_bytes(2, 'little'))   # Bits per sample
        # Data chunk
        f.write(b'data')
        f.write((0).to_bytes(4, 'little'))  # No data
    print(f"Created {sound}")

print("\nAll assets created successfully!")
print("You can now run the game with: python ChessGUI.py\n")

# Clean up pygame
pygame.quit()
