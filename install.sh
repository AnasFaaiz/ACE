#!/bin/bash
# ==============================================================================
# A.C.E. (Automated Command Environment) Installation Script v3 - Latest
# This script is idempotent, meaning it can be run multiple times safely.
# It will clean up old configurations and install the latest version.
# ==============================================================================

# --- Helper Functions for Colored Output ---
echo_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
echo_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
echo_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }
echo_warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }

# --- Error Handling ---
set -e  # Exit on any error

# --- Main Installation Logic ---
echo_info "Starting A.C.E. installation..."

# 1. Find the project's root directory (handle symlinks properly)
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
    SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$SCRIPT_DIR/$SOURCE"
done
ACE_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

echo_info "A.C.E. project found at: $ACE_DIR"

# 2. Verify required files exist
LAUNCHER_PATH="$ACE_DIR/ace_launcher.sh"
MAIN_PY_PATH="$ACE_DIR/src/main.py"

if [ ! -f "$LAUNCHER_PATH" ]; then
    echo_error "ace_launcher.sh not found at $LAUNCHER_PATH"
    echo_error "Please ensure you're running this script from the A.C.E. project directory."
    exit 1
fi

if [ ! -f "$MAIN_PY_PATH" ]; then
    echo_error "main.py not found at $MAIN_PY_PATH"
    echo_error "Please ensure the A.C.E. project structure is intact."
    exit 1
fi

# 3. Set up the global 'ace' command
COMMAND_DIR="$HOME/.local/bin"
ACE_COMMAND_PATH="$COMMAND_DIR/ace"

mkdir -p "$COMMAND_DIR"
echo_info "Ensuring command directory exists at $COMMAND_DIR"

# Make launcher executable
chmod +x "$LAUNCHER_PATH"
echo_info "Made ace_launcher.sh executable"

# Remove old symlink if it exists (even if broken)
if [ -L "$ACE_COMMAND_PATH" ] || [ -e "$ACE_COMMAND_PATH" ]; then
    echo_info "Removing existing 'ace' command..."
    rm -f "$ACE_COMMAND_PATH"
fi

# Create new symlink
ln -sf "$LAUNCHER_PATH" "$ACE_COMMAND_PATH"
echo_success "Created global 'ace' command linking to $LAUNCHER_PATH"

# 4. Detect the user's shell and configure it
SHELL_CONFIG_FILE=""
CURRENT_SHELL=$(basename "$SHELL")

case "$CURRENT_SHELL" in
    "zsh")
        SHELL_CONFIG_FILE="$HOME/.zshrc"
        echo_info "Zsh shell detected. Configuring $SHELL_CONFIG_FILE"
        ;;
    "bash")
        SHELL_CONFIG_FILE="$HOME/.bashrc"
        echo_info "Bash shell detected. Configuring $SHELL_CONFIG_FILE"
        ;;
    *)
        echo_warn "Shell '$CURRENT_SHELL' not automatically supported. Please manually configure your PATH and 'acego' function."
        ;;
esac

if [ -n "$SHELL_CONFIG_FILE" ]; then
    # Create config file if it doesn't exist
    touch "$SHELL_CONFIG_FILE"
    
    # --- Configure PATH ---
    PATH_CONFIG_LINE='export PATH="$HOME/.local/bin:$PATH"'
    if ! grep -qF "$PATH_CONFIG_LINE" "$SHELL_CONFIG_FILE"; then
        echo_info "Adding ~/.local/bin to your PATH..."
        echo "" >> "$SHELL_CONFIG_FILE"
        echo "# Add A.C.E. command directory to PATH" >> "$SHELL_CONFIG_FILE"
        echo "$PATH_CONFIG_LINE" >> "$SHELL_CONFIG_FILE"
        echo_success "~/.local/bin added to PATH."
    else
        echo_info "~/.local/bin is already in your PATH."
    fi
    
    # --- Configure acego Function (Clean Slate Method) ---
    ACEGO_START_MARKER="# --- A.C.E. acego Function START ---"
    ACEGO_END_MARKER="# --- A.C.E. acego Function END ---"
    
    # Remove any old acego block to ensure a clean slate
    if grep -qF "$ACEGO_START_MARKER" "$SHELL_CONFIG_FILE"; then
        echo_info "Found old 'acego' configuration. Removing it..."
        # Use a more portable sed command
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "/$ACEGO_START_MARKER/,/$ACEGO_END_MARKER/d" "$SHELL_CONFIG_FILE"
        else
            # Linux
            sed -i "/$ACEGO_START_MARKER/,/$ACEGO_END_MARKER/d" "$SHELL_CONFIG_FILE"
        fi
    fi
    
    # Add the new, correct acego function
    echo_info "Adding 'acego' function to your shell configuration..."
    cat >> "$SHELL_CONFIG_FILE" << 'EOF'

# --- A.C.E. acego Function START ---
acego() {
    if [ $# -eq 0 ]; then
        echo "Usage: acego <project_name>"
        echo "Navigate to a project directory using A.C.E."
        return 1
    fi
    
    PROJECT_PATH=$(ace project go "$1" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$PROJECT_PATH" ]; then
        cd "$PROJECT_PATH"
        echo "Switched to: $PROJECT_PATH"
    else
        echo "Project '$1' not found or error occurred."
        return 1
    fi
}
# --- A.C.E. acego Function END ---
EOF
    echo_success "'acego' function configured successfully."
fi

# 5. Verify installation
echo_info "Verifying installation..."

# Test if ace command is accessible
export PATH="$HOME/.local/bin:$PATH"
if command -v ace >/dev/null 2>&1; then
    echo_success "✓ 'ace' command is accessible"
else
    echo_error "✗ 'ace' command is not accessible"
fi

# Test if ace_launcher.sh is executable
if [ -x "$LAUNCHER_PATH" ]; then
    echo_success "✓ ace_launcher.sh is executable"
else
    echo_error "✗ ace_launcher.sh is not executable"
fi

echo ""
echo_success "Installation complete!"
echo_info "Next steps:"
echo_info "  1. Restart your terminal or run: source $SHELL_CONFIG_FILE"
echo_info "  2. Test with: ace --help"
echo_info "  3. Navigate to projects with: acego <project_name>"
echo ""
echo_warn "If you encounter issues, ensure Python 3 is installed and the A.C.E. project structure is intact."

