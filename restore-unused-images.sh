#!/bin/bash

# Log file from the move operation
MOVE_LOG="unused_images.log"
RESTORE_LOG="restore_unused_images.log"
UNUSED_DIR="unused_images"

if [ ! -f "$MOVE_LOG" ]; then
  echo "❌ Move log '$MOVE_LOG' not found. Nothing to restore."
  exit 1
fi

echo "♻️ Restoring unused images to original locations..."
> "$RESTORE_LOG"

while IFS= read -r line; do
    # Expecting lines like: Moved: static/images/old-icon.png -> unused_images/static/images/old-icon.png
    src=$(echo "$line" | cut -d'>' -f2 | xargs)  # Trim whitespace
    dest=$(echo "$line" | cut -d':' -f2 | cut -d'-' -f1 | xargs)

    if [ -f "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        mv "$src" "$dest"
        echo "Restored: $src -> $dest" >> "$RESTORE_LOG"
    else
        echo "⚠️ File not found: $src" >> "$RESTORE_LOG"
    fi
done < "$MOVE_LOG"

echo "✅ Restore complete."
echo "📄 Restore log: $RESTORE_LOG"
