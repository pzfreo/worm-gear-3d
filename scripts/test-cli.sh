#!/bin/bash
# Test CLI with example JSON files
# Usage: ./scripts/test-cli.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
EXAMPLES_DIR="$PROJECT_DIR/examples"

# Create temp directory for output
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "Testing wormgear-geometry CLI..."
echo "Output directory: $TEMP_DIR"
echo ""

# Test 1: 7mm globoid worm
echo "Test 1: 7mm globoid worm gear (examples/7mm-globoid.json)"
echo "  This tests: globoid worm, ddcut anti-rotation, virtual hobbing"
wormgear-geometry "$EXAMPLES_DIR/7mm-globoid.json" --output-dir "$TEMP_DIR" --no-view
if [ -f "$TEMP_DIR/worm_m0.5_z1.step" ] && [ -f "$TEMP_DIR/wheel_m0.5_z13.step" ]; then
    echo "  ✓ STEP files generated successfully"
    ls -la "$TEMP_DIR"/*.step
else
    echo "  ✗ FAILED: STEP files not found"
    exit 1
fi

echo ""
echo "All tests passed!"
