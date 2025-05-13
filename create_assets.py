import pygame
import os

# Initialize pygame
pygame.init()

# Set up display (we need this to create surfaces)
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Asset Generator")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (210, 180, 140)  # Tan color for background

# Create directories if they don't exist
os.makedirs('pieces', exist_ok=True)
os.makedirs('sounds', exist_ok=True)

# Generate piece images
piece_symbols = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # White pieces
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'   # Black pieces
}

# Image size
img_size = 100
font = pygame.font.SysFont('arial', 75, bold=True)

print("Generating chess pieces...")

# Generate all pieces
for piece in piece_symbols:
    # Create a surface with transparency
    surf = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))  # Transparent background
    
    # Add a colored circle
    circle_color = BACKGROUND
    pygame.draw.circle(surf, circle_color, (img_size//2, img_size//2), img_size//2 - 5)
    
    # Add piece symbol
    is_white = piece.isupper()
    text_color = WHITE if is_white else BLACK
    text_surf = font.render(piece_symbols[piece], True, text_color)
    text_rect = text_surf.get_rect(center=(img_size//2, img_size//2))
    surf.blit(text_surf, text_rect)
    
    # Save image
    pygame.image.save(surf, os.path.join('pieces', f"{piece}.png"))
    print(f"Created {piece}.png")

# Create simple sound files (empty WAV files)
print("\nCreating sound files...")
sound_files = ['move.wav', 'capture.wav', 'check.wav', 'game_over.wav']

for sound_file in sound_files:
    # Create a minimal valid WAV file
    with open(os.path.join('sounds', sound_file), 'wb') as f:
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
    
    print(f"Created {sound_file}")

print("\nDone! Now you can run ChessGUI.py")
pygame.quit()
