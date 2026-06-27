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

## 30-Day Improvement Plan (April 2026)

This section captures the current, implementation-focused roadmap for improving reliability, architecture, and practical AI capabilities in A.C.E.

### Plan Goals

1. Stabilize command execution and response behavior across CLI and API.
2. Improve security and data integrity in feature modules.
3. Deliver practical AI upgrades (better intent matching, persistent memory, and training data readiness).
4. Keep scope realistic for 30 days while preparing for a stronger model-based phase after this window.

### Phase 1 (Days 1-5): Command and Reliability Foundation

1. Unify command routing so command behavior is defined in one place.
2. Standardize response and error shape for CLI/API compatibility.
3. Remove unsafe shell execution patterns and add subprocess timeouts.

Primary files:
- `src/dispatcher.py`
- `src/agent/commands.py`
- `src/api.py`
- `src/features/dashboard_manager.py`
- `src/features/project_scaffolder.py`

### Phase 2 (Days 6-12): Data and State Robustness

1. Harden persistence flows for project and schedule data.
2. Introduce safer read/write behavior (atomic writes and validation).
3. Add structured logging for command, duration, and failure categories.

Primary files:
- `src/features/project_manager.py`
- `src/features/task_scheduler.py`
- `src/features/vanguard.py`
- `src/dispatcher.py`

### Phase 3 (Days 13-20): Practical AI Upgrades

1. Replace token-overlap intent scoring with stronger fuzzy matching and confidence thresholds.
2. Persist agent memory across restarts (instead of process-only memory).
3. Populate `training_data.jsonl` with labeled examples for current command set.
4. Improve next-action recommendations using recent command patterns and confidence.

Primary files:
- `src/agent/intent.py`
- `src/agent/memory.py`
- `src/agent/recommend.py`
- `training_data.jsonl`

### Phase 4 (Days 21-26): Voice and API Consistency

1. Improve voice error handling and fallback behavior.
2. Ensure API capability reporting and validation are consistent with dispatcher behavior.

Primary files:
- `src/features/voice_handler.py`
- `src/api.py`
- `src/dispatcher.py`

### Phase 5 (Days 27-30): Finalization and Documentation

1. Regression checks for core flows (project, news, overview, scheduler, backup, dashboard).
2. Validate web-safe command constraints in API mode.
3. Align all documentation with implemented behavior and known limitations.

### AI Status Update

Current state:
1. AI behavior is mostly heuristic and rule-based.
2. Intent parsing exists but is simplistic (token overlap).
3. Agent memory exists but is currently in-memory only.
4. Voice support exists via SpeechRecognition and pyttsx3.

30-day AI outcome target:
1. More robust intent recognition through fuzzy matching and confidence handling.
2. Persistent short-term memory for better continuity.
3. Usable labeled dataset in `training_data.jsonl` for next-stage model fine-tuning.
4. Better suggestion quality and safer fallback behavior.

### Post-30-Day AI Direction (Next Stage)

After this roadmap is complete, the next major AI step is model-backed intent classification and richer semantic recommendations.

Candidate path:
1. Fine-tune a lightweight classifier (for example DistilBERT) on collected intent data.
2. Add confidence-based fallback to heuristic matching.
3. Introduce embedding-based recommendation ranking for next actions.
4. Evaluate intent quality with a labeled holdout set before enabling by default.

### Verification Checklist

1. Command regression pass: project register/list/go/create, news, overview, schedule add/list/remove, backup, dashboard.
2. API regression pass: schema consistency and web-safe behavior.
3. Input validation pass: malformed paths, invalid schedule payloads, unsupported command text.
4. Persistence pass: repeated writes do not corrupt `projects.json` or `schedule.json`.
5. AI quality pass: measurable improvement in intent-match success over the baseline.
