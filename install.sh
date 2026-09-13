#!/usr/bin/env bash
# Standalone 1-line installer for agy-guard
set -euo pipefail

# Auto-detect Termux environment ($PREFIX/bin) vs standard Linux/macOS ($HOME/.local/bin)
if [ -n "${PREFIX:-}" ] && [ -d "${PREFIX}/bin" ]; then
    DEFAULT_DIR="${PREFIX}/bin"
    IS_TERMUX=1
else
    DEFAULT_DIR="$HOME/.local/bin"
    IS_TERMUX=0
fi

INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_DIR}"
mkdir -p "$INSTALL_DIR"

echo "==> Installing agy-guard to $INSTALL_DIR/agy-guard..."
curl -fsSL https://raw.githubusercontent.com/zyekhabdul/agy-guard/main/bin/agy-guard -o "$INSTALL_DIR/agy-guard"
chmod +x "$INSTALL_DIR/agy-guard"

echo "==> Checking Python dependencies..."
if ! command -v python3 >/dev/null 2>&1; then
    if [ "$IS_TERMUX" -eq 1 ]; then
        echo "[ NOTE ] Installing python via pkg in Termux..."
        pkg install -y python
    else
        echo "[ NOTE ] 'python3' is required. Please install python3 via your package manager."
    fi
fi

echo "==> Installation complete! Run 'agy-guard' or add $INSTALL_DIR to your PATH if not already present."
