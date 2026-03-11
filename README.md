# A.C.E. — Automated Command Environment

> **Your personal AI-powered developer assistant that lives in the terminal.**  
A.C.E. understands your intentions, automates your workflow, manages your projects, and provides a unified command ecosystem — all from the command line.

[![Open Source](https://img.shields.io/badge/Open%20Source-❤️-red.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8+-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-lightgrey.svg)]()

---

## 🚀 What is A.C.E.?

A.C.E. (**Automated Command Environment**) is an extensible, modular, terminal-based assistant designed to supercharge developer productivity.

It acts as a **central command hub**, helping you:

- Manage and navigate projects  
- Automate Git workflows  
- Fetch tech news  
- Run scheduled tasks  
- Launch a full tmux dashboard  
- Back up your projects  
- Scaffold new project templates  

A.C.E. doesn’t just run commands — it **reduces friction**, understands your workflow, and feels like a teammate inside your terminal.

---

## 📦 Installation

A.C.E. runs on **Linux**, **macOS**, and **Windows (via WSL)**.  
Setup takes under a minute.

---

## ✅ System Requirements

### Required
- Python **3.8+**
- Git
- Standard Unix tools (`sed`, `grep`, `ln`)

### Optional (Recommended)
- `tmux` — enables the dashboard  
- Audio libraries — for future voice features  

### Installing System Dependencies

#### tmux (Required for Dashboard Features)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tmux
```

**macOS:**
```bash
brew install tmux
```

**Fedora/CentOS/RHEL:**
```bash
sudo dnf install tmux
# or for older versions: sudo yum install tmux
```

**Arch Linux:**
```bash
sudo pacman -S tmux
```

#### Audio Dependencies (Optional - for Voice Features)
If you want to use voice features, install system audio libraries:

**Ubuntu/Debian:**
```bash
sudo apt install portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
```

**Fedora/CentOS:**
```bash
sudo dnf install python3-pyaudio portaudio-devel
```

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/AnasFaaiz/ace-system.git
cd ace-system
```

#### 2. Install Python Dependencies
The `requirements.txt` file contains all necessary Python packages:
```bash
pip3 install -r requirements.txt
```

**What gets installed:**
- `requests` - For making HTTP requests to APIs (GitHub, News)
- `python-dotenv` - For securely loading credentials from .env file  
- `feedparser` - For parsing RSS feeds in the News Hub feature
- `schedule` - For the Task Scheduler feature
- `SpeechRecognition` - For speech-to-text (optional voice features)
- `pyttsx3` - For text-to-speech (optional voice features)  
- `PyAudio` - For microphone access (required by SpeechRecognition)

**Note:** If you encounter issues with audio packages (PyAudio, SpeechRecognition, pyttsx3), you can install only the core dependencies:

```bash
# Core dependencies only (recommended for most users)
pip3 install requests python-dotenv feedparser schedule

# Full installation with voice features (requires audio system setup)
pip3 install -r requirements.txt
```

#### 3. Run the Automated Installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Create a global `ace` command
- Add `~/.local/bin` to your PATH
- Install the `acego` navigation function
- Verify the installation

#### 4. Reload Your Shell
```bash
source ~/.zshrc  # or ~/.bashrc for Bash users
# OR simply restart your terminal
```

### Verify Installation
```bash
# Test the ace command
ace --help

# Test project navigation
acego --help
```

That's it! A.C.E. is now installed globally and ready to use from anywhere in your terminal.

---

## Core Features

A.C.E. is a feature-rich suite of tools designed to supercharge your development process.

### 1. Workspace & Project Management
* **Project Scaffolder (`ace project create`):** Instantly create new project structures from predefined templates for modern tech stacks (React, Python, Next.js, etc.).
* **Project Registry (`ace project register`, `ace project list`):** A.C.E. maintains a `projects.json` memory file of all your projects. It can automatically scan existing local Git repositories, discover corresponding GitHub URLs via the API, and register them for future use.
* **Quick Navigation (`acego <project>`):** A special shell function that allows you to instantly `cd` into any registered project directory, no matter where you are in the filesystem.

### 2. The Vanguard (Intelligent Git Assistant)
* **Interactive Save (`ace save`):** A safe and powerful workflow that shows you a status of your changes, asks for confirmation, and then automatically runs `git add .`, `git commit`, and `git push` to your current feature branch. Includes safety locks to prevent accidental pushes to `main`.
* **Mission Control Overview (`ace overview`):** A multi-threaded command that runs in parallel to give you a near-instant, high-level summary of Git status and most recent commits for all registered projects.

### 3. Information & Automation Hub
* **Tech News Tracker (`ace news`):** Fetch the latest trending headlines from developer-focused sources like Hacker News directly in your terminal, with options to filter by source.
* **Task Scheduler (`ace schedule`, `ace scheduler`):** An internal cron-like system. Schedule any A.C.E. command to run at specific times, list scheduled jobs, and run a persistent watcher process to execute them automatically.

### 4. The tmux Dashboard
* **One-Command Environment (`ace dashboard start`):** Instantly launches a persistent, multi-pane `tmux` session pre-configured as your development dashboard. Provides auto-updating panes for Git Overview and Tech News, alongside a main workspace for active development.

### 5. Backup System

* **ace backup** — Backup all registered projects
* **ace backup <nickname>** — Backup one project
* Backups include commit hash & timestamp.

---

## Architecture Overview

A.C.E. is built using a professional, modular Python package structure designed for maintainability and extensibility.

```
ace-system/
├── src/
│   ├── main.py              # Entry point and command router
│   ├── features/            # Modular feature implementations
│   │   ├── project_manager.py
│   │   ├── vanguard.py
│   │   ├── news_hub.py
│   │   ├── backup_manager.py
│   │   └── task_scheduler.py
│   └── utils/               # Shared utilities
├── ace_launcher.sh          # Global command launcher
├── install.sh               # Automated installer
├── requirements.txt         # Python dependencies
├── projects.json            # Project registry (created on first use)
├── schedule.json            # Task scheduler data
└── .env                     # Secure credential storage
```

**Key Components:**
- **`/src/main.py`**: Command parser and feature dispatcher
- **`/src/features/`**: Modular feature implementations for easy extension
- **`projects.json` & `schedule.json`**: A.C.E.'s persistent memory
- **`.env`**: Secure storage for API tokens and credentials

---

## Usage Examples

Once installed, interact with A.C.E. from anywhere in your terminal:

```bash
# Get a high-level overview of all your projects
ace overview

# Register a new project for quick access
ace project register /path/to/my-project my-nickname

# Save your work with intelligent Git workflow
ace save my-project-nickname

# Instantly navigate to any registered project
acego my-project-nickname

# Create a new project from templates
ace project create my-new-app --template react

# Stay updated with tech news
ace news --source hackernews

# Schedule automated tasks
ace schedule "ace overview" --daily --time 09:00

# Launch your persistent mission control dashboard
ace dashboard start

# Backups
ace backup
ace backup my-app
```

---

## Configuration

### Setting up GitHub Integration
For full project management features, configure your GitHub token:

```bash
# Create a .env file in the A.C.E. directory
echo "GITHUB_USERNAME='your_username' > .env
echo "GITHUB_TOKEN=your_github_personal_access_token_here" > .env
```


## Troubleshooting

### Common Installation Issues

#### PyAudio Installation Fails
```bash
# Install system audio dependencies first (see Audio Dependencies section above)
# Then try installing just core dependencies:
pip3 install requests python-dotenv feedparser schedule
```

#### tmux Command Not Found
```bash
# Install tmux using your system package manager (see tmux installation section above)
```

#### ace Command Not Found After Installation
```bash
# Ensure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

---

## Contributing

A.C.E. is an open-source project and contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/ace-system.git
cd ace-system

# Install development dependencies
pip3 install -r requirements.txt

# Install in development mode
./install.sh

# Make changes and test
ace --help
```

---

## System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.7 or higher
- **Dependencies**: See `requirements.txt`
- **Optional**: tmux (for dashboard features)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with Python and love for the developer community
- Inspired by the need for intelligent terminal workflows
- Special thanks to all contributors and users who help make A.C.E. better

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ace-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ace-system/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/ace-system/wiki)

---

*A.C.E. - Because your terminal should be as smart as you are.*
