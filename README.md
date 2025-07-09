# A.C.E. - Automated Command Environment

> A personalized AI assistant that lives in your terminal, designed to understand natural language and automate your daily developer tasks.

---

### What is A.C.E.?

A.C.E. (Automated Command Environment) is a powerful command-line tool built with Python, designed to act as a centralized hub for developers. It streamlines workflows, manages projects, and keeps you informed, all without leaving the comfort of your terminal.

The core philosophy behind A.C.E. is to create an intelligent assistant that you can collaborate with, moving beyond simple scripts to a system that understands your intent.

---

### Core Features

A.C.E. is being built with a rich set of features to supercharge your development process.

#### Workspace Management
* **Project Scaffolder (`ace project create`):** Instantly create new project structures from predefined templates for different tech stacks (e.g., React, Python, Next.js).
* **Project Registry (`ace project register`, `list`, `remove`):** A.C.E. maintains a memory of all your projects. It can automatically scan an existing local Git repository, discover its corresponding GitHub URL via the API, and register it for future use.
* **Quick Navigation (`acego`):** A special shell helper function that allows you to instantly `cd` into any of your registered project directories, no matter where you are in the filesystem.

#### The Vanguard (Git Integration)
* **Smart Workflow Automation (`ace git activate`):** An interactive workflow that shows you a status of your changes, asks for confirmation, and then automatically runs `git add .`, `git commit`, and `git push` to your current feature branch. It includes a safety lock to prevent accidental pushes to `main` or `master`.
* **Synchronization (`ace git sync`):** Safely pull the latest changes from your remote repository to keep your local project up-to-date.

#### Information Hub
* **Tech News Tracker (`ace news`):** Fetch the latest trending headlines from developer-focused sources like Hacker News directly in your terminal.
* **Task Scheduler (`ace schedule`):** Schedule any A.C.E. command to run at a later time, helping you automate cleanup tasks and reminders.

---

### Architecture Overview

A.C.E. is built using a professional, modular Python package structure to ensure it's easy to maintain and extend.

* **`/src/main.py`**: The main entry point that parses terminal commands.
* **`/src/features/`**: A dedicated "toolbox" where each file is a separate module responsible for a specific skill (e.g., `project_manager.py`, `vanguard.py`).
* **`projects.json`**: A local JSON file that acts as A.C.E.'s memory, storing details about all managed projects.

---

### Usage Examples

Once installed, you can interact with A.C.E. from anywhere in your terminal.

```bash
# List all projects A.C.E. is managing
ace project list

# Register an existing project located at a specific path
ace project register /path/to/my/project

# Instantly navigate to a registered project's directory
acego my-project-nickname

# Get the latest tech news
ace news
