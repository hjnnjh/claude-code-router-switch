#!/bin/bash

set -e

APP_NAME="ccr-switch"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
CMD_NAME="ccrswitch"

# ANSI colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing $APP_NAME...${NC}"

# 1. Pre-flight checks
echo "Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Warning: python3 not found.${NC} It is required for the helper script."
fi

if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}Warning: 'uv' not found.${NC} It is required to run the scripts."
    echo "Please install it: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

if ! command -v ccr &> /dev/null; then
    echo -e "${YELLOW}Warning: 'ccr' command not found.${NC} Please ensure Claude Code Router is installed."
fi

# 2. Setup Directories
echo "Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# 3. Copy Files
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$SOURCE_DIR/sync_ccr.sh" ] || [ ! -f "$SOURCE_DIR/ccr_helper.py" ]; then
    echo -e "${RED}Error: Source files (sync_ccr.sh, ccr_helper.py) not found in $SOURCE_DIR${NC}"
    exit 1
fi

echo "Copying files to $INSTALL_DIR..."
cp "$SOURCE_DIR/sync_ccr.sh" "$INSTALL_DIR/"
cp "$SOURCE_DIR/ccr_helper.py" "$INSTALL_DIR/"

# 4. Create Wrapper
WRAPPER_PATH="$BIN_DIR/$CMD_NAME"
echo "Creating global command '$CMD_NAME' at $WRAPPER_PATH..."

cat > "$WRAPPER_PATH" <<EOF
#!/bin/bash
exec "$INSTALL_DIR/sync_ccr.sh" "\$@"
EOF

# 5. Permissions
chmod +x "$INSTALL_DIR/sync_ccr.sh"
chmod +x "$WRAPPER_PATH"

# 6. Check PATH
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) echo -e "${YELLOW}Warning: $BIN_DIR is not in your PATH.${NC}" ;;
esac

echo "--------------------------------------------------"
echo -e "${GREEN}✅ Installation successful!${NC}"
echo ""
echo "You can now run the tool using the command:"
echo -e "  ${GREEN}$CMD_NAME${NC}"
echo ""
echo "Installed files:"
echo "  - Script:  $INSTALL_DIR/sync_ccr.sh"
echo "  - Wrapper: $WRAPPER_PATH"
echo "--------------------------------------------------"
