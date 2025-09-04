#!/bin/bash
# ==============================================================================
# A.C.E. (Automated Command Environment) Launcher Script (v2 - Robust)
# This script is the entry point for the global 'ace' command.
# It correctly finds the project's root directory, even when called via a symbolic link.
# ==============================================================================

# Find the real directory of this script, following any symbolic links.
# This is the most reliable way to locate the project root.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$SCRIPT_DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"


# Construct the full path to the main Python script.
MAIN_PY_PATH="$SCRIPT_DIR/src/main.py"

# Execute the main Python script using python3.
# The special "$@" variable passes along all the arguments you typed after 'ace'.
python3 "$MAIN_PY_PATH" "$@"

