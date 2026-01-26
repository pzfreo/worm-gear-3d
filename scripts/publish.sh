#!/bin/bash
# Publish script for wormgear package
# Usage: ./scripts/publish.sh [version]
# Example: ./scripts/publish.sh 0.0.4
# If no version provided, increments patch version automatically

set -e

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "Current version: $CURRENT_VERSION"

if [ -n "$1" ]; then
    NEW_VERSION="$1"
else
    # Auto-increment patch version
    IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
    PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
fi

echo "New version: $NEW_VERSION"

# Confirm
read -p "Publish version $NEW_VERSION? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Update version in pyproject.toml
sed -i.bak "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
rm -f pyproject.toml.bak

# Commit version bump
git add pyproject.toml
git commit -m "chore: Bump version to $NEW_VERSION"

# Create and push tag
git tag "v$NEW_VERSION"
git push origin main
git push origin "v$NEW_VERSION"

echo ""
echo "Published v$NEW_VERSION!"
echo "GitHub Action will build and upload to PyPI."
echo "Check: https://github.com/pzfreo/wormgear/actions"
