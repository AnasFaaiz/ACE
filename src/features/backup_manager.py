import os
import tarfile
import datetime
from src.features import project_manager

BACKUP_ROOT = os.path.expanduser("~/Documents/ACE_BACKUPS")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_commit_hash(project_path):
    import subprocess
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

def create_backup_filename(nickname, commit_hash):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    ensure_dir(os.path.join(BACKUP_ROOT, today))
    return os.path.join(BACKUP_ROOT, today, f"{nickname}-{commit_hash}.tar.gz")

def backup_single_project(nickname, project_path):
    commit_hash = get_commit_hash(project_path)
    backup_file = create_backup_filename(nickname, commit_hash)

    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(project_path, arcname=nickname)

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

