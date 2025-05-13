#!/usr/bin/env python

import os
import sys
import subprocess

print("Chess Game Launcher")
print("------------------")

required_files = [
    "ChessGUI.py",
    "ChessGame.py", 
    "ChessBoard.py",
    "Node.py"
]

# Check if all required files exist
missing_files = [f for f in required_files if not os.path.exists(f)]
if missing_files:
    print(f"Error: Missing required files: {', '.join(missing_files)}")
    input("Press Enter to exit...")
    sys.exit(1)

# Check if asset directories exist
if not os.path.exists("pieces") or not os.path.exists("sounds") or len(os.listdir("pieces")) < 12:
    print("Creating chess assets (pieces and sounds)...")
    try:
        subprocess.run([sys.executable, "create_assets.py"], check=True)
    except Exception as e:
        print(f"Error creating assets: {e}")
        print("You may need to run 'create_assets.py' manually.")

# Launch the chess GUI
print("Starting Chess Game...")
try:
    subprocess.run([sys.executable, "ChessGUI.py"])
except Exception as e:
    print(f"Error launching game: {e}")
    input("Press Enter to exit...")
    sys.exit(1)
