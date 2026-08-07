import os
import tarfile
import datetime
import subprocess
from src.features import project_manager

BACKUP_ROOT = os.path.expanduser("~/Documents/ACE_BACKUPS")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_commit_hash(project_path):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except:
        return "no-git"

def get_valid_git_files(project_path):
    """
        Queries Git for all files that are not ignored by .gitignore
        Returns a list of relative file paths.
    """
    try:
        # 1. Get alll files tracked by Git
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=project_path, stdout=subprocess.PIPE, text=True, check=True
        ).stdout.splitlines()
            
        # 2. Get untracked files 
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=project_path, stdout=subprocess.PIPE, text=True, check=True
        ).stdout.splitlines()

        return tracked + untracked
    except subprocess.CalledProcessError:
        return None
def backup_single_project(nickname, project_path):
    commit_hash = get_commit_hash(project_path)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    ensure_dir(os.path.join(BACKUP_ROOT, today))
    
    # Creates one single .tar.xz file (not a folder)
    backup_file = os.path.join(BACKUP_ROOT, today, f"{nickname}-{commit_hash}.tar.xz")

    files_to_backup = get_valid_git_files(project_path)
    
    if files_to_backup is None:
        return f"[SKIP] {nickname} is not a Git repository. Cannot parse .gitignore."

    # preset=9 gives maximum LZMA2 compression
    with tarfile.open(backup_file, "w:xz", preset=9) as tar:
        for file_rel_path in files_to_backup:
            abs_path = os.path.join(project_path, file_rel_path)
            
            # arcname structures the files inside the archive neatly under the project's nickname
            tar.add(abs_path, arcname=os.path.join(nickname, file_rel_path))

    return f"[OK] {nickname} → {backup_file}"

def backup_all_projects():
    projects = project_manager.load_projects()

    if not projects:
        return "[INFO] No registered projects to back up."

    results = []
    for nickname, info in projects.items():
        path = info.get("local_path")

        if not os.path.exists(path):
            results.append(f"[SKIP] {nickname} → path missing")
            continue

        results.append(backup_single_project(nickname, path))

    return "\n".join(results)
