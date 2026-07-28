# A.C.E. — Automated Command Environment

> **Your personal developer assistant that lives in the terminal.**
> A.C.E. manages your projects, automates your Git workflow, runs scheduled tasks, and gives you a unified command ecosystem — all from the command line.

[![CI](https://github.com/AnasFaaiz/ACE/actions/workflows/ci.yml/badge.svg)](https://github.com/AnasFaaiz/ACE/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)]()
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

A.C.E. doesn't just run commands — it **reduces friction**, understands your workflow, and feels like a teammate inside your terminal.

---

## ✅ Requirements

### Required

- **Python 3.10+**
- **Git**
- **pipx** — recommended installer (keeps A.C.E. in its own isolated environment)

### Optional

- **tmux** — enables the `ace dashboard` feature
- Audio libraries — for experimental voice features

### Installing pipx

**Arch Linux:**
```bash
sudo pacman -S python-pipx
```

**Ubuntu/Debian:**
```bash
sudo apt install pipx
```

**macOS:**
```bash
brew install pipx
```

Then make sure pipx's bin directory is on your PATH:
```bash
pipx ensurepath
```

Restart your shell afterwards.

### Installing tmux (Required for Dashboard Features)

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

### Audio Dependencies (Optional — Experimental)

Voice features are experimental and not installed by default. If you want to
experiment with them, install your system's audio libraries first:

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

---

## 📦 Installation

### Option 1 — Install a released version

```bash
pipx install git+https://github.com/AnasFaaiz/ACE@v0.2.0
```

### Option 2 — Install from source (for development)

```bash
git clone https://github.com/AnasFaaiz/ACE.git
cd ACE
pipx install --editable .
```

`--editable` links the install to your working copy, so code changes take
effect immediately without reinstalling.

### Set up the `acego` navigation function

```bash
ace shell-init --install
source ~/.zshrc     # or ~/.bashrc
```

**Why this step is separate:** `acego` changes your shell's working directory,
and a child process can never change its parent's directory. That makes it a
shell *function* rather than an executable, and shell functions have to be
defined by your shell's startup file. `ace shell-init --install` writes the
function into your rc file between marker comments, so re-running it after an
upgrade replaces the block instead of duplicating it.

Prefer to see what it writes first?

```bash
ace shell-init              # prints the function, changes nothing
```

Or source it live instead of embedding it, by adding this line to your rc file:

```bash
eval "$(ace shell-init --shell zsh)"
```

### Verify

```bash
ace --version
ace --help
type acego        # → "acego is a shell function from ~/.zshrc"
```

---

## Python Dependencies

Installed automatically by pipx. Declared in `pyproject.toml`:

| Package | Purpose |
|---|---|
| `requests` | HTTP calls to the GitHub and news APIs |
| `python-dotenv` | Loads credentials from `.env` |
| `feedparser` | Parses RSS feeds for the News Hub |
| `schedule` | Powers the task scheduler |
| `textual` | Renders the TUI dashboard |

---

## Core Features

### 1. Workspace & Project Management

* **Project Scaffolder (`ace project create`):** Instantly create new project structures from predefined templates for modern tech stacks (React, Next.js, Vite, Python).
* **Project Registry (`ace project register`, `ace project list`):** A.C.E. maintains a registry of all your projects. It scans existing local Git repositories, discovers corresponding GitHub URLs via the API, and can create the remote repo for you if it doesn't exist yet.
* **Quick Navigation (`acego <project>`):** A shell function that instantly `cd`s into any registered project directory, no matter where you are in the filesystem.

### 2. The Vanguard (Intelligent Git Assistant)

* **Interactive Save (`ace save`):** Shows a status of your changes, asks for confirmation, then runs `git add .`, `git commit`, and `git push` to your current feature branch. Includes safety locks to prevent accidental pushes to `main`.
* **Mission Control Overview (`ace overview`):** A multi-threaded command that runs in parallel to give a near-instant summary of Git status and recent commits across all registered projects.

### 3. Information & Automation Hub

* **Tech News Tracker (`ace news`):** Fetch trending headlines from developer-focused sources like Hacker News, with options for source and fetch method (RSS, API, or scrape).
* **Task Scheduler (`ace schedule`, `ace scheduler`):** An internal cron-like system. Schedule any A.C.E. command to run at a given time, list scheduled jobs, and run a persistent watcher process to execute them.

### 4. The tmux Dashboard

* **One-Command Environment (`ace dashboard start`):** Instantly launches a persistent, multi-pane `tmux` session pre-configured as your development dashboard. Provides auto-updating panes for Git Overview and Tech News, alongside a main workspace for active development.

### 5. The TUI

* **`ace tui`** — a full Textual interface over the same features, for when you'd rather browse than type.

### 6. Backup System

* **`ace backup`** — back up all registered projects
* **`ace backup <nickname>`** — back up one project
* Backups include commit hash & timestamp.

---

## Architecture Overview

```
ACE/
├── .github/
│   └── workflows/
│       ├── ci.yml               # Test matrix across Python 3.10–3.14
│       └── release.yml          # Tag-triggered build + GitHub Release
├── config/
│   └── settings.toml            # Application configuration
├── data/
│   ├── project.json             # Project registry
│   └── schedule.json            # Scheduled task store
├── src/
│   ├── main.py                  # Entry point and command router
│   ├── shell.py                 # acego shell function + rc-file installer
│   ├── core/                    # Application internals
│   │   ├── config.py            # Settings loading
│   │   ├── context.py           # Shared runtime context
│   │   ├── memory.py            # Persistence layer
│   │   └── service_manager.py   # Service lifecycle
│   ├── features/                # Modular feature implementations
│   │   ├── project_manager.py
│   │   ├── project_scaffolder.py
│   │   ├── vanguard.py
│   │   ├── news_hub.py
│   │   ├── backup_manager.py
│   │   ├── dashboard_manager.py
│   │   ├── task_scheduler.py
│   │   └── voice_handler.py     # Experimental
│   ├── tui/                     # Textual dashboard
│   │   ├── app.py
│   │   ├── screens/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── tools/
│   │   └── widgets/
│   └── utils/
│       └── helpers.py
├── pyproject.toml               # Package metadata, dependencies, entry point
├── CHANGELOG.md
└── .env                         # Secure credential storage (git-ignored)
```

**Key components:**

- **`src/main.py`** — argparse command parser and feature dispatcher
- **`src/shell.py`** — the `acego` snippet and the logic that installs it
- **`src/core/`** — configuration, context, and service management
- **`src/features/`** — one module per feature, lazily imported so startup stays fast
- **`data/`** — A.C.E.'s persistent memory; git-ignored, created on first use
- **`.env`** — GitHub credentials; git-ignored, never commit this

---

## Usage Examples

```bash
# Register a project (nickname is taken from the directory name)
ace project register /path/to/my-project

# List everything A.C.E. knows about
ace project list

# Jump to a project from anywhere
acego my-project

# Scaffold a new project from a template
ace project create my-new-app

# High-level Git status across all projects
ace overview

# Save your work with the intelligent Git workflow
ace save my-project

# Tech news
ace news --source hackernews --limit 10 --method rss

# Schedule a command, then run the watcher
ace schedule add "09:00" "ace overview"
ace schedule list
ace scheduler start

# Launch the tmux mission control dashboard
ace dashboard start

# Launch the TUI
ace tui

# Backups
ace backup
ace backup my-project
```

---

## Configuration

### GitHub Integration

Project registration queries the GitHub API to find (or create) the matching
remote repository. Create a `.env` file in the A.C.E. directory:

```bash
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_github_personal_access_token
```

The token needs `repo` scope. **`.env` is git-ignored — never commit it.**
If you ever push a token by accident, revoke it on GitHub rather than just
deleting the file.

### Application Settings

Non-secret configuration lives in `config/settings.toml`.

---

## Upgrading

```bash
cd /path/to/ACE
git pull
pipx install --editable . --force
ace shell-init --install       # refresh the acego block if it changed
source ~/.zshrc
```

Editable installs pick up code changes automatically, but a version bump in
`pyproject.toml` requires the reinstall for `ace --version` to report it.

---

## Troubleshooting

#### `ace: command not found`

```bash
pipx ensurepath
# then restart your shell, or:
export PATH="$HOME/.local/bin:$PATH"
```

#### `acego: command not found`

The function isn't defined in your shell. Run:

```bash
ace shell-init --install
source ~/.zshrc
type acego        # should report a shell function
```

#### `acego` cds to the wrong place, or errors with a usage dump

Your rc file holds an old copy of the function. Re-run `ace shell-init --install`
(it should say **updated**, not *installed*) and re-source your rc file. If it
says *installed*, check for a duplicate block:

```bash
grep -c "acego START" ~/.zshrc      # should be 1
```

#### `externally-managed-environment` during install

Arch and Debian block system-wide `pip install` (PEP 668). Use pipx, as above.

#### `tmux: command not found`

Install tmux with your system package manager (see the requirements section).

---

## Development

```bash
git clone https://github.com/AnasFaaiz/ACE.git
cd ACE
pipx install --editable .
ace shell-init --install
```

CI runs on every push to `main`, testing installation and CLI startup across
Python 3.10 through 3.14.

### Cutting a release

```bash
# 1. Bump version in pyproject.toml
# 2. Move [Unreleased] into a dated section in CHANGELOG.md
git commit -am "release: 0.3.0"
git tag -a v0.3.0 -m "0.3.0"
git push && git push --tags
```

The release workflow verifies the tag matches `pyproject.toml`, builds the
wheel and sdist, and publishes a GitHub Release with both attached.

---

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- **Issues**: [GitHub Issues](https://github.com/AnasFaaiz/ACE/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AnasFaaiz/ACE/discussions)

---

*A.C.E. — Because your terminal should be as smart as you are.*
