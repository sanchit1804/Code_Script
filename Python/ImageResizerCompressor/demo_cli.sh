#!/bin/bash
# Quick demonstration script for CLI interface

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        CLI Interface - Quick Demo                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.x"
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import PIL; import cv2; import numpy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ All dependencies installed"
else
    echo "⚠ Some dependencies missing. Installing..."
    pip3 install -r requirements.txt
fi
echo ""

# Show folder structure
echo "📂 Folder Structure:"
echo "├── ingest/  (INPUT: Place your images here)"
echo "├── output/  (OUTPUT: Processed images saved here)"
echo "└── config.json (Saved configurations)"
echo ""

# Check for images in ingest folder
image_count=$(find ingest -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.webp" -o -iname "*.tiff" \) 2>/dev/null | wc -l)

if [ "$image_count" -gt 0 ]; then
    echo "✓ Found $image_count image(s) in ingest folder"
    echo ""
    echo "📋 Available Commands:"
    echo ""
    echo "1️⃣  Interactive Mode (Recommended):"
    echo "   python3 cli_interface.py"
    echo ""
    echo "2️⃣  Use a Preset:"
    echo "   python3 cli_interface.py --config web"
    echo ""
    echo "3️⃣  Custom Parameters:"
    echo "   python3 cli_interface.py --width 800 --quality 85"
    echo ""
    echo "4️⃣  List All Configurations:"
    echo "   python3 cli_interface.py --list-configs"
    echo ""
    echo "▶ Ready to process! Choose a command above."
else
    echo "⚠ No images found in ingest folder"
    echo ""
    echo "📥 To get started:"
    echo "1. Copy images to ingest folder:"
    echo "   cp ~/Pictures/*.jpg ingest/"
    echo ""
    echo "2. Run the CLI interface:"
    echo "   python3 cli_interface.py"
    echo ""
    echo "Or run this demo script again after adding images."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Offer to list configurations
read -p "Would you like to see available configurations? (y/n): " response
if [[ "$response" == "y" ]]; then
    echo ""
    python3 cli_interface.py --list-configs
fi

echo ""
echo "✨ Demo complete!"
