#!/usr/bin/env bash
# Links this repo's User folder into Sublime Text on macOS.
# Package Control installs the listed packages the next time Sublime starts.
set -euo pipefail

REPO_USER="$(cd "$(dirname "$0")" && pwd)/User"
PACKAGES="$HOME/Library/Application Support/Sublime Text/Packages"
TARGET="$PACKAGES/User"

if pgrep -q "Sublime Text"; then
    echo "Quit Sublime Text first." >&2
    exit 1
fi

mkdir -p "$PACKAGES"

if [ -L "$TARGET" ]; then
    echo "Replacing existing symlink: $(readlink "$TARGET")"
    rm "$TARGET"
elif [ -e "$TARGET" ]; then
    BACKUP="$TARGET.backup-$(date +%Y%m%d-%H%M%S)"
    echo "Backing up existing User folder to: $BACKUP"
    mv "$TARGET" "$BACKUP"
fi

ln -s "$REPO_USER" "$TARGET"
echo "Linked $TARGET -> $REPO_USER"
echo "Next: open Sublime, install Package Control (Cmd+Shift+P > Install Package Control) if needed, then restart."
