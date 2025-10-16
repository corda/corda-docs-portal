#!/bin/bash

# Define extensions
IMAGE_EXTENSIONS="png|jpg|jpeg|webp|gif"

# Folder to move unused images into
UNUSED_DIR="unused_images"

# Create the destination directory
mkdir -p "$UNUSED_DIR"

echo "🔍 Scanning for unused images in static/, assets/, and content/..."

# Step 1: Get all image file paths from static/, assets/, content/
find static/ assets/ content/ -type f | grep -Ei "\.($IMAGE_EXTENSIONS)$" > all_images.txt

# Step 2: Find image references in templates, content, and other source files
grep -rhoEi "\S+\.(png|jpg|jpeg|webp|gif)" content/ layouts/ assets/ > used_images_raw.txt

# Step 3: Normalize used image names to just the filename (basename)
awk -F/ '{print $NF}' used_images_raw.txt | sort | uniq > used_image_names.txt

# Step 4: Compare & move unused images
> unused_images.txt
> unused_images.log

echo "🚚 Moving unused images to $UNUSED_DIR/..."

while IFS= read -r filepath; do
    filename=$(basename "$filepath")
    if ! grep -Fxq "$filename" used_image_names.txt; then
        echo "$filepath" >> unused_images.txt
        
        # Preserve directory structure inside the unused folder
        target_path="$UNUSED_DIR/$filepath"
        mkdir -p "$(dirname "$target_path")"
        
        mv "$filepath" "$target_path"
        echo "Moved: $filepath -> $target_path" >> unused_images.log
    fi
done < all_images.txt

# Summary
echo "✅ Done."
echo "📁 Unused images listed in: unused_images.txt"
echo "📄 Move log: unused_images.log"
wc -l unused_images.txt | awk '{print "🧹 Total unused images moved: "$1}'
