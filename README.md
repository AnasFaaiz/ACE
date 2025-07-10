# A.C.E. - Automated Command Environment

> A personalized AI assistant that lives in your terminal, designed to understand natural language and automate your daily developer tasks.

---

### What is A.C.E.?

A.C.E. (Automated Command Environment) is a powerful command-line tool built with Python, designed to act as a centralized hub for developers. It streamlines workflows, manages projects, keeps you informed, and even provides a full "mission control" dashboard, all without leaving the comfort of your terminal.

The core philosophy behind A.C.E. is to create an intelligent assistant that you can collaborate with, moving beyond simple scripts to a system that understands your intent.

---

### Core Features

A.C.E. is a feature-rich suite of tools designed to supercharge your development process.

#### 1. Workspace & Project Management
* **Project Scaffolder (`ace project create`):** Instantly create new project structures from predefined templates for modern tech stacks (e.g., React, Python, Next.js).
* **Project Registry (`ace project register`, `list`):** A.C.E. maintains a `projects.json` memory file of all your projects. It can automatically scan an existing local Git repository, discover its corresponding GitHub URL via the API, and register it for future use.
* **Quick Navigation (`acego`):** A special shell helper function that allows you to instantly `cd` into any of your registered project directories, no matter where you are in the filesystem.

#### 2. The Vanguard (Intelligent Git Assistant)
* **Interactive Save (`ace save`):** A safe and powerful workflow that shows you a status of your changes, asks for confirmation, and then automatically runs `git add .`, `git commit`, and `git push` to your current feature branch. It includes a safety lock to prevent accidental pushes to `main`.
* **Mission Control Overview (`ace overview`):** A multi-threaded command that runs in parallel to give you a near-instant, high-level summary of the Git status and most recent commit for all of your registered projects.

#### 3. Information & Automation Hub
* **Tech News Tracker (`ace news`):** Fetch the latest trending headlines from developer-focused sources like Hacker News directly in your terminal, with options to filter by source.
* **Task Scheduler (`ace schedule`, `ace scheduler`):** An internal cron-like system. Schedule any A.C.E. command to run at a later time, list your scheduled jobs, and run a persistent watcher process to execute them.

#### 4. The `tmux` Dashboard
* **One-Command Environment (`ace dashboard start`):** Instantly launches a persistent, multi-pane `tmux` session pre-configured to act as your development dashboard. It provides auto-updating panes for your Git Overview and Tech News, alongside a main workspace for your active development.

---

### Architecture Overview

A.C.E. is built using a professional, modular Python package structure to ensure it's easy to maintain and extend.

* **`/src/main.py`**: The main entry point that parses terminal commands and acts as a "switchboard."
* **`/src/features/`**: A dedicated "toolbox" where each `.py` file is a separate module responsible for a specific skill (e.g., `project_manager.py`, `vanguard.py`).
* **`projects.json` & `schedule.json`**: Local JSON files that act as A.C.E.'s memory.
* **`.env`**: Securely stores secret credentials like your `GITHUB_TOKEN`.

---

### Usage Examples

Once installed, you can interact with A.C.E. from anywhere in your terminal.

```bash
# Get a high-level overview of all your projects
ace overview

# Save your work on a registered project
ace save my-project-nickname

# Instantly navigate to a registered project's directory
acego my-project-nickname

# Launch your persistent mission control dashboard
ace dashboard start
