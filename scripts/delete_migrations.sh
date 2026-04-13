#!/bin/bash

# Set the target directory
TARGET_DIR="backend"

# Find and delete all migration files except __init__.py
find "$TARGET_DIR" -path "*/migrations/*.py" ! -name "__init__.py" -type f -delete
find "$TARGET_DIR" -path "*/migrations/*.pyc" -type f -delete

# Print completion message
echo "All migration files (except __init__.py) have been deleted from $TARGET_DIR."
