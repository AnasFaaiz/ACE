import subprocess
import time
import os
import sys

# The name we will give our tmux session.
SESSION_NAME = "ACE"
# Get the absolute path to the ACE project's home directory.
ACE_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def run_tmux_command(command):
    """A helper function to run a tmux command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing tmux command: {e}")
        return False
    return True

def start_dashboard():
    """Creates and configures the A.C.E. tmux dashboard session."""

    check_session_cmd = f"tmux has-session -t {SESSION_NAME}"
    session_exists = subprocess.run(check_session_cmd, shell=True, capture_output=True).returncode == 0

    if session_exists:
        print(f"Dashboard session '{SESSION_NAME}' already exists. Attaching...")
        os.system(f"tmux attach-session -t {SESSION_NAME}")
        return

    print(f"--- Launching A.C.E. Dashboard in new tmux session: '{SESSION_NAME}' ---")

    # Create the new, detached tmux session.
    run_tmux_command(f"tmux new-session -d -s {SESSION_NAME}")

    # --- THE CORRECTED LAYOUT LOGIC ---
    # 1. Split the main window (pane 0) vertically. This creates a new pane (pane 1) on the right.
    #    The '-p 60' flag makes the new right-hand pane take up 60% of the space.
    run_tmux_command(f"tmux split-window -h -p 60 -t {SESSION_NAME}:0.0")

    # 2. Now, target the original, smaller pane on the left (pane 0) and split it horizontally.
    #    This creates a new pane (pane 2) below it.
    run_tmux_command(f"tmux split-window -v -t {SESSION_NAME}:0.0")

    # Our final pane layout is:
    # Pane 0: Main Workspace (Right side)
    # Pane 1: News Hub (Top-Left)
    # Pane 2: Git Overview (Bottom-Left)

    # Build the full, direct command for Python to avoid PATH issues.
    python_executable = sys.executable
    # We must use the absolute path to main.py for reliability inside tmux.
    main_script_path = os.path.join(ACE_HOME, 'src', 'main.py')
    base_command = f"'{python_executable}' '{main_script_path}'"

    # 3. Send the commands to the correct panes.
    
    # Send the news command to the Top-Left pane (pane 1).
    print("Configuring News Hub pane...")
    news_command = f"watch -n 300 {base_command} news"
    run_tmux_command(f"tmux send-keys -t {SESSION_NAME}:0.1 \"{news_command}\" C-m")

    # Send the overview command to the Bottom-Left pane (pane 2).
    print("Configuring Git Overview pane...")
    overview_command = f"watch -n 60 {base_command} overview"
    run_tmux_command(f"tmux send-keys -t {SESSION_NAME}:0.2 \"{overview_command}\" C-m")

    # Select the main workspace pane (pane 0) so the cursor is there when you start.
    run_tmux_command(f"tmux select-pane -t {SESSION_NAME}:0.0")

    # Attach to the new session to make it visible.
    print("Attaching to session...")
    time.sleep(1)
    os.system(f"tmux attach-session -t {SESSION_NAME}")


