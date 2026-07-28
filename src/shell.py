"""Shell integration for A.C.E. — the acego navigation function.

acego must be a shell *function*, not an executable: only code running
inside your shell can change the shell's working directory.
"""
import os
import re
from pathlib import Path

try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("ace-cli")
    except PackageNotFoundError:
        __version__ = "dev"
except ImportError:
    __version__ = "dev"


START = "# --- A.C.E. acego START (v{v}) ---"
START_RE = r"# --- A\.C\.E\. acego START.*?---"
END = "# --- A.C.E. acego END ---"

RC_FILES = {
    "zsh": "~/.zshrc",
    "bash": "~/.bashrc",
    "fish": "~/.config/fish/config.fish",
}

POSIX = r'''acego() {
    case "$1" in
        ""|-h|--help)
            echo "usage: acego <nickname>   jump to a registered project"
            echo "       acego -l           list registered projects"
            return 0
            ;;
        -l|--list)
            ace project nicknames
            return 0
            ;;
    esac
    local target
    target="$(ace project go -- "$1")" || return 1
    cd "$target" && echo "→ $target"
}'''

FISH = r'''function acego
    switch "$argv[1]"
        case "" -h --help
            echo "usage: acego <nickname>   jump to a registered project"
            echo "       acego -l           list registered projects"
            return 0
        case -l --list
            ace project nicknames
            return 0
    end
    set -l target (ace project go -- $argv[1]); or return 1
    cd $target; and echo "→ $target"
end'''

def detect_shell():
    """Best guess at the user's shell from $SHELL."""
    name = Path(os.environ.get("SHELL", "")).name
    return name if name in RC_FILES else "bash"


def snippet(shell):
    return FISH if shell == "fish" else POSIX


def block(shell):
    """The snippet wrapped in versioned markers."""
    return f"{START.format(v=__version__)}\n{snippet(shell)}\n{END}\n"


def install(shell):
    """Write (or refresh) the acego block in the user's rc file.

    Idempotent: an existing block is replaced, never duplicated.
    Returns (rc_path, action) where action is 'installed' or 'updated'.
    """
    rc = Path(RC_FILES[shell]).expanduser()
    rc.parent.mkdir(parents=True, exist_ok=True)
    text = rc.read_text() if rc.exists() else ""

    pattern = START_RE + r".*?" + re.escape(END) + r"\n?"

    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, block(shell), text, flags=re.S)
        action = "updated"
    else:
        text = text.rstrip("\n") + "\n\n" + block(shell)
        action = "installed"

    rc.write_text(text)
    return rc, action
