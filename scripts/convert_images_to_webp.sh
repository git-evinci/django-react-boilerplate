#!/bin/bash

# Recursively find and convert JPG, JPEG, and PNG images in 'static/' directories to WebP
# Requires: `cwebp` (part of Google's WebP tools)

# Set the quality (adjustable, default 80)
QUALITY=80

# Function to convert images
convert_to_webp() {
    local file="$1"
    local output="${file%.*}.webp"

    # Skip if WebP version already exists
    if [ -f "$output" ]; then
        echo "Skipping: $output already exists."
        return
    fi

    echo "Converting: $file -> $output"
    cwebp -q $QUALITY "$file" -o "$output"

    # Optional: Remove original image after conversion (uncomment to enable)
    # rm "$file"
}

export -f convert_to_webp

# Find JPG, JPEG, PNG files inside "static/" directories and convert them
find . -type d -name "staticfiles" -print0 | while IFS= read -r -d '' static_dir; do
    find "$static_dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) -print0 | while IFS= read -r -d '' file; do
        convert_to_webp "$file"
    done
done

echo "Conversion completed!"
