# GEMINI.md

## Project Overview

This project, A.C.E. (Automated Command Environment), is a Python-based command-line tool that acts as a personal AI assistant for developers. It's designed to streamline workflows, manage projects, and provide a "mission control" dashboard in the terminal.

The project is structured as a modular Python application with a clear separation of concerns. The main entry point is `src/main.py`, which uses `argparse` to handle command-line arguments and dispatch commands to various feature modules located in the `src/features/` directory.

**Key Technologies:**

*   **Python 3.7+**
*   **Shell scripting (Bash)** for installation and command launching.
*   **`argparse`** for command-line interface.
*   **`requests`** for making HTTP requests to APIs (e.g., GitHub, news sources).
*   **`python-dotenv`** for managing environment variables.
*   **`feedparser`** for parsing RSS feeds.
*   **`schedule`** for task scheduling.
*   **(Optional) `tmux`** for the dashboard feature.

**Architecture:**

The project follows a modular architecture:

*   `ace_launcher.sh`: The global command launcher.
*   `install.sh`: The automated installer.
*   `src/main.py`: The entry point and command router.
*   `src/features/`: Contains individual feature modules (e.g., `project_manager.py`, `news_hub.py`).
*   `projects.json`: A file to store registered project information.
*   `schedule.json`: A file to store scheduled tasks.
*   `.env`: For storing sensitive information like API tokens.

## Building and Running

**Installation:**

1.  **Clone the repository.**
2.  **Install Python dependencies:**
    ```bash
    pip3 install -r requirement.txt
    ```
3.  **Run the installer:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
4.  **Reload your shell:**
    ```bash
    source ~/.zshrc  # or ~/.bashrc
    ```

**Running:**

The `ace` command is globally available after installation.

**Core Commands:**

*   `ace --help`: Display help information.
*   `ace project create <name>`: Create a new project from a template.
*   `ace project register <path>`: Register a project.
*   `ace project list`: List registered projects.
*   `acego <project_name>`: Navigate to a registered project.
*   `ace news`: Fetch tech news.
*   `ace save <project_name>`: Save project work using Git.
*   `ace overview`: Get a high-level overview of all registered Git projects.
*   `ace schedule add "<time_string>" "<command_string>"`: Schedule a command.
*   `ace schedule list`: List scheduled commands.
*   `ace dashboard start`: Start the tmux dashboard.

## Development Conventions

*   **Modular Design:** Features are implemented in separate modules within the `src/features/` directory.
*   **Command-Line Interface:** The `argparse` library is used to define and manage the CLI.
*   **Shell Scripts:** Shell scripts are used for installation and launching the application, ensuring portability across Linux, macOS, and WSL.
*   **JSON for Data Persistence:** `projects.json` and `schedule.json` are used to store application data.
*   **Environment Variables:** The `.env` file is used for storing sensitive information like API keys, following best practices for security.
*   **Testing:** (TODO: No explicit testing framework is mentioned in the provided files. It would be beneficial to add a testing framework like `pytest` and create a `tests/` directory.)
