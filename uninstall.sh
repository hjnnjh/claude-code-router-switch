#!/bin/bash

set -e

APP_NAME="ccr-switch"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
CMD_NAME="ccrswitch"

echo "Uninstalling $APP_NAME..."

rm -f "$BIN_DIR/$CMD_NAME"
rm -rf "$INSTALL_DIR"

echo "✅ Uninstallation complete."
