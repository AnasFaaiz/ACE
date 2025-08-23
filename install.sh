#!/bin/bash

# --- Helper Functions for colored output ---
echo_info() {
    # Blue color for informational messages
    printf "\033[1;34m%s\033[0m\n" "$1"
}

echo_success() {
    # Green color for success messages
    printf "\033[1;32m%s\033[0m\n" "$1"
}

echo_warning() {
    # Yellow color for warnings
    printf "\033[1;33m%s\033[0m\n" "$1"
}


# --- Main Installation Logic ---
echo_info "Starting A.C.E. installation..."

# 1. Get the absolute path to the directory where this script is located.
# This will be the root of the A.C.E. project.
ACE_HOME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo_info "A.C.E. project found at: $ACE_HOME_DIR"

# 2. Define the path for the global commands. ~/.local/bin is a standard location.
BIN_DIR="$HOME/.local/bin"
LAUNCHER_PATH="$ACE_HOME_DIR/ace_launcher.sh"
ACE_COMMAND_PATH="$BIN_DIR/ace"

# Create the ~/.local/bin directory if it doesn't exist.
mkdir -p "$BIN_DIR"
echo_info "Ensuring command directory exists at $BIN_DIR"

# 3. Create the symbolic link for the 'ace' command.
# This points the global 'ace' command to our launcher script.
if [ -L "$ACE_COMMAND_PATH" ]; then
    echo_warning "Existing 'ace' command found. Overwriting..."
    rm "$ACE_COMMAND_PATH"
fi
ln -s "$LAUNCHER_PATH" "$ACE_COMMAND_PATH"
echo_info "Created global 'ace' command."

# 4. Detect the user's shell and set the correct configuration file.
SHELL_CONFIG_FILE=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG_FILE="$HOME/.zshrc"
    echo_info "Zsh shell detected. Configuring $SHELL_CONFIG_FILE"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG_FILE="$HOME/.bashrc"
    echo_info "Bash shell detected. Configuring $SHELL_CONFIG_FILE"
else
    echo_warning "Could not automatically detect shell. You may need to manually add the functions to your shell's config file."
fi

# 5. Add the necessary configurations to the shell config file.
if [ -n "$SHELL_CONFIG_FILE" ]; then
    # Check if the PATH is already configured to avoid duplicates.
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG_FILE"; then
        echo_info "Adding ~/.local/bin to your PATH..."
        echo '' >> "$SHELL_CONFIG_FILE"
        echo '# Add A.C.E. command directory to PATH' >> "$SHELL_CONFIG_FILE"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG_FILE"
    else
        echo_info "~/.local/bin is already in your PATH."
    fi

    # Check if the acego function is already configured.
    if ! grep -q 'acego()' "$SHELL_CONFIG_FILE"; then
        echo_info "Adding 'acego' function to your shell..."
        # We use 'cat <<EOF' to safely append a multi-line block of text.
        cat <<EOF >> "$SHELL_CONFIG_FILE"

# Custom A.C.E. function for project navigation
acego() {
    ORIGINAL_DIR=\$(pwd)
    ACE_HOME="$ACE_HOME_DIR"
    
    DESTINATION=\$(cd "\$ACE_HOME" && python3 -m src.main project go "\$1")
    
    cd "\$ORIGINAL_DIR"
    
    if [ -n "\$DESTINATION" ]; then
        cd "\$DESTINATION"
    fi
}
EOF
    else
        echo_info "'acego' function is already configured."
    fi
fi

echo_success "\nInstallation complete!"
echo_warning "Please restart your terminal or run 'source $SHELL_CONFIG_FILE' for the changes to take effect."



