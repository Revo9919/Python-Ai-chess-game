#!/usr/bin/env python
"""
Chess Game Launcher
------------------
This script ensures all assets are properly created before launching the chess GUI.
"""

import os
import sys

# Check if pygame is installed and install it if not
try:
    import pygame
except ImportError:
    print("Pygame is not installed. Attempting to install it...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame has been installed successfully!")
        import pygame
    except Exception as e:
        print(f"Failed to install pygame: {e}")
        print("Please install pygame manually using: pip install pygame")
        input("Press Enter to exit...")
        sys.exit(1)

# Initialize pygame for creating assets
pygame.init()
pygame.font.init()

def create_piece_images():
    """Create chess piece images if they don't exist"""
    from ChessGUI import create_piece_image
    
    PIECE_SIZE = 64  # Standard piece size
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    
    # Ensure pieces directory exists
    os.makedirs("pieces", exist_ok=True)
    
    print("Checking chess piece images...")
    
    # Check if all pieces exist, create if missing
    missing = False
    for piece in pieces:
        img_path = os.path.join("pieces", f"{piece}.png")
        if not os.path.exists(img_path):
            print(f"Creating image for {piece}...")
            img = create_piece_image(piece, PIECE_SIZE)
            pygame.image.save(img, img_path)
            missing = True
    
    if missing:
        print("Created missing piece images successfully.")
    else:
        print("All piece images are already available.")

def create_sound_files():
    """Create empty sound files if they don't exist"""
    os.makedirs("sounds", exist_ok=True)
    
    # Check for sound files
    sound_files = ["move.wav", "capture.wav", "check.wav", "game_over.wav"]
    missing = False
    
    for sound in sound_files:
        sound_path = os.path.join("sounds", sound)
        if not os.path.exists(sound_path):
            print(f"Creating placeholder sound file: {sound}")
            # Create a minimal valid WAV file
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
            missing = True
    
    if missing:
        print("Created missing sound files successfully.")
    else:
        print("All sound files are already available.")

def main():
    """Prepare assets and launch the chess GUI"""
    print("\nChess Game Launcher")
    print("------------------")

    # Check if we have the required files
    required_files = ["ChessBoard.py", "ChessGame.py", "ChessGUI.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: Required file {file} not found!")
            input("Press Enter to exit...")
            return 1

    try:
        # Create required assets
        create_sound_files()
        create_piece_images()
        
        # Launch the GUI
        print("\nStarting Chess Game...\n")
        from ChessGUI import main as start_gui
        start_gui()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nAn error occurred. Press Enter to exit...")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
