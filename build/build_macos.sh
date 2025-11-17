#!/bin/bash
# macOS Build Script for Test Pattern Player

echo "============================================"
echo "Building Test Pattern Player for macOS..."
echo "============================================"
echo ""

# Check if we're in the build directory
if [ ! -f "build_macos.sh" ]; then
    echo "Error: Please run this script from the build/ directory"
    exit 1
fi

# Go to parent directory
cd ..

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/build
rm -rf build/dist
rm -f build/*.spec

# Create .icns file for macOS (if on macOS and iconutil is available)
if command -v iconutil &> /dev/null; then
    echo "Creating macOS icon (.icns)..."
    cd resources/icons
    if [ ! -d "icon.iconset" ]; then
        mkdir icon.iconset
        cp icon_16x16.png icon.iconset/icon_16x16.png
        cp icon_32x32.png icon.iconset/icon_16x16@2x.png
        cp icon_32x32.png icon.iconset/icon_32x32.png
        cp icon_64x64.png icon.iconset/icon_32x32@2x.png
        cp icon_128x128.png icon.iconset/icon_128x128.png
        cp icon_256x256.png icon.iconset/icon_128x128@2x.png
        cp icon_256x256.png icon.iconset/icon_256x256.png
        cp icon_512x512.png icon.iconset/icon_256x256@2x.png
        cp icon_512x512.png icon.iconset/icon_512x512.png
        cp icon_1024x1024.png icon.iconset/icon_512x512@2x.png
    fi
    iconutil -c icns icon.iconset
    cd ../..
    ICON_PATH="resources/icons/icon.icns"
else
    echo "Warning: iconutil not found. Using PNG icon instead."
    ICON_PATH="resources/icons/icon.png"
fi

# Build application
echo ""
echo "Building macOS application..."
pyinstaller --name "TestPatternPlayer" \
            --windowed \
            --onefile \
            --icon="$ICON_PATH" \
            --add-data "resources:resources" \
            --add-data "data:data" \
            --noconfirm \
            main.py

# Move build artifacts
mv dist build/
mv *.spec build/

echo ""
echo "============================================"
echo "Build complete!"
echo "Application: build/dist/TestPatternPlayer.app"
echo "============================================"
echo ""
echo "To run the app:"
echo "  open build/dist/TestPatternPlayer.app"
echo ""
