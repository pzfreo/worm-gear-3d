#!/bin/bash
# Vercel build script for wormgear web interface
# Copies Python package to web/wormgear for WASM/Pyodide access

set -e  # Exit on error

echo "🔧 Building wormgear web interface..."

# Ensure we're in the web directory
cd "$(dirname "$0")"

# Copy wormgear package from parent src/ to web/wormgear/ (gitignored)
echo "📦 Copying wormgear package..."
if [ -d "../src/wormgear" ]; then
    # Remove old copy if exists
    rm -rf wormgear

    # Copy unified package (NOT to src/, that was the old broken pattern)
    cp -r ../src/wormgear .

    # Remove Python cache files (not needed in browser)
    find wormgear -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find wormgear -name "*.pyc" -delete 2>/dev/null || true

    echo "✓ Copied wormgear package to web/wormgear/"
else
    echo "❌ Error: ../src/wormgear not found"
    exit 1
fi

# Verify critical calculator files exist (web uses calculator module only)
echo "🔍 Verifying calculator files..."
REQUIRED_FILES=(
    "wormgear/__init__.py"
    "wormgear/calculator/__init__.py"
    "wormgear/calculator/core.py"
    "wormgear/calculator/validation.py"
    "wormgear/calculator/output.py"
    "wormgear/calculator/js_bridge.py"
    "wormgear/calculator/json_schema.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✓ All required calculator files present"

# List what was copied
echo ""
echo "📋 Calculator package contents:"
ls -lh wormgear/calculator/

echo ""
echo "✅ Build complete!"
echo "📝 Note: web/wormgear/ is a build artifact (gitignored)"
