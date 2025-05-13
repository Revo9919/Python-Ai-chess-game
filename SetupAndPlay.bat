@echo off
echo Chess Game Launcher
echo ------------------

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install Python 3.x and try again.
    pause
    exit /b 1
)

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame not found. Installing pygame...
    python -m pip install pygame
    if %errorlevel% neq 0 (
        echo Failed to install pygame. Please try running: pip install pygame
        pause
        exit /b 1
    )
)

REM Launch the game
echo Starting Chess Game...
python launch_chess.py
pause
