#!/bin/bash
# Vercel build script for wormgear web interface
# Copies Python package to web/wormgear for WASM access (build artifact, gitignored)

set -e  # Exit on error

echo "🔧 Building wormgear web interface..."

# Ensure we're in the web directory
cd "$(dirname "$0")"

# Remove old build artifact
rm -rf wormgear

# Copy unified package from src/
echo "📦 Copying wormgear package..."
if [ -d "../src/wormgear" ]; then
    cp -r ../src/wormgear .

    # Clean Python cache files (not needed in browser)
    find wormgear -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find wormgear -name "*.pyc" -delete 2>/dev/null || true

    echo "✓ Copied wormgear package to web/wormgear/"
else
    echo "❌ Error: ../src/wormgear not found"
    exit 1
fi

# Verify required files for web calculator
echo "🔍 Verifying calculator files..."
REQUIRED_FILES=(
    "wormgear/__init__.py"
    "wormgear/enums.py"
    "wormgear/calculator/__init__.py"
    "wormgear/calculator/core.py"
    "wormgear/calculator/validation.py"
    "wormgear/calculator/output.py"
    "wormgear/io/__init__.py"
    "wormgear/io/loaders.py"
    "wormgear/io/schema.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        exit 1
    fi
done

echo "✓ All calculator files present"

echo ""
echo "✅ Build complete!"
