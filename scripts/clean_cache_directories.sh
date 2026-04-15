#!/bin/bash

# Script to recursively delete cache files and directories in a Django project

# Directories and files to clean
CACHE_ITEMS=(
    ".mypy_cache"
    ".ruff_cache"
    "__pycache__"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    ".coverage"
    "htmlcov"
    ".hypothesis"
    ".pytest_cache"
    "celerybeat-schedule"
    "*.egg-info"
    "build"
    "dist"
    ".cache"
    ".ipynb_checkpoints"
    #"db.sqlite3"  # Often used in development
)

# Function to delete cache items
clean_caches() {
    for ITEM in "${CACHE_ITEMS[@]}"; do
        echo "Searching for $ITEM..."
        # Handle directories
        find . -type d -name "$ITEM" -exec rm -rf {} + 2>/dev/null
        # Handle files (for patterns like *.pyc)
        find . -type f -name "$ITEM" -exec rm -f {} + 2>/dev/null
        echo "$ITEM deleted."
    done
}

# Main execution
echo "Starting Django project cleanup in $(pwd)..."
clean_caches
echo "Cleanup completed!"
