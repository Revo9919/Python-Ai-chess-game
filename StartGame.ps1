# Chess Game Setup and Launcher (PowerShell)
Write-Host "Chess Game Launcher" -ForegroundColor Cyan
Write-Host "------------------" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found! Please install Python 3.x and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pygame is installed
Write-Host "Checking for pygame..." -ForegroundColor Yellow
$pygameInstalled = python -c "try: import pygame; print('Pygame found'); exit(0)\nexcept: exit(1)" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pygame not found. Installing pygame..." -ForegroundColor Yellow
    python -m pip install pygame
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install pygame. Please try running: pip install pygame" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        Write-Host "Pygame installed successfully!" -ForegroundColor Green
    }
} else {
    Write-Host "Pygame is already installed." -ForegroundColor Green
}

# Create missing image files for black pieces
Write-Host "Checking for missing piece images..." -ForegroundColor Yellow
if (!(Test-Path pieces)) {
    New-Item -ItemType Directory -Path pieces | Out-Null
    Write-Host "Created pieces directory." -ForegroundColor Yellow
}

# Check for black pieces specifically
$blackPieces = @('b', 'k', 'n', 'p', 'q', 'r')
$missingPieces = $false

foreach ($piece in $blackPieces) {
    if (!(Test-Path "pieces\$piece.png")) {
        $missingPieces = $true
        Write-Host "Missing piece image for: $piece" -ForegroundColor Yellow
    }
}

if ($missingPieces) {
    Write-Host "Some piece images are missing. Running create_assets.py..." -ForegroundColor Yellow
    try {
        python create_assets.py
    } catch {
        Write-Host "Error creating assets. We'll continue anyway." -ForegroundColor Yellow
    }
}

# Launch the game
Write-Host ""
Write-Host "Starting Chess Game..." -ForegroundColor Cyan
python launch_chess.py

Read-Host "Press Enter to exit"
