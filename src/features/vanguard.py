import os
import subprocess
import json
import concurrent.futures

ACE_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECTS_FILE = os.path.join(ACE_ROOT_DIR, "projects.json")

def run_command(command, cwd):
    """
    Runs a terminal command in a  specified directory (cwd) and returns its output.
    """
    result = subprocess.run(
        command, 
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None

def check_project_status(project_info):
    """
    Checks the Git status and last commit for a single project.
    Thhis is the function that each thread will run in parallel.
    """

    # Unpack project
    nickname, details = project_info
    project_path = details['local_path']

    if not os.path.isdir(project_path):
        return f"\n   - {nickname}:\n    Status: Path not found."

    # Use git status
    status, error = run_command("git  status --porcelain", cwd=project_path)
    if error:
        return f"  - {nickname}:\n  Status: Not a Git repository."

    status_summary = " Up to date"
    if status:
        status_summary = " Uncommitted changes"

    last_commit, error = run_command('git log -n 1 --pretty=format:"%s (%cr)"', cwd=project_path)
    if error:
        last_commit = "No commits found"

    return f"   - {nickname}:\n  Status: {status_summary}\n   Last Commit: {last_commit}"

def generate_git_overview():
    """
    Fetches the status of all registered projects in parallel using threads.
    """
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        return "Project registry not found. Please register a project first."

    if not projects:
        return "No projects are registered with A.C.E. yet"

    print("--- Git Project Overview")


    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(check_project_status, projects.items())

        for result in results:
            print(result)

    print("---------------------------")
    return ""

def save_workflow(nickname):
    """
    Handles the 'ace save' workflow for specfic project nickname.
    It's and interactive "precaution mode" assisstant.
    """
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        return "Project registry not found. Please register project."

    if nickname not in projects:
        return f"Error: Project '{nickname}' not found in registry."

    project_path = projects[nickname]['local_path']
    print(f"--- Vanguard activating for project: '{nickname}' ---")
    print(f"Working inside: {project_path}")


    # 2. Run safety check & workflow inside the project's directory

    _, error = run_command("git rev-parse --is-inside-work-tree", cwd=project_path)
    if error:
        return "This directory is not a git repository"

    current_branch, error = run_command("git rev-parse --abbrev-ref HEAD", cwd=project_path)
    if error:
        return f"Could not determine current branch: {error}"

    if current_branch in ["main", "master"]:
         return f"\n⚠️  SAFETY ENGAGED: Cannot save directly on the '{current_branch}' branch."
    print(f"Current branch: '{current_branch}'")
    print("\n--- Review Your Chanegs ---")
    status_output, _ = run_command("git status", cwd=project_path)
    print(status_output)
    print("--------------------------")

    if "nothing to commit, working tree clean" in status_output:
        return "Workspace is clean. Nothing to save."
    
    proceed = input("Proceed to stage and commit? [Y/n] ").lower().strip()
    if proceed not in ['y', 'yes', '']:
        return "Save workflow cancelled by user"
    commit_message = input("Enter your commit message: ")
    if not commit_message:
        return "Commit message cannot be empty. Aborting."

    print("\nStep 1: Staging all changes...")
    _, error = run_command("git add .", cwd=project_path)
    if error: return f"Error staging files: {error}"
    print("...Done.")

    print("\nStep 2: Committing changes...")
    commit_command = f'git commit -m "{commit_message}"'
    _, error = run_command(commit_command, cwd=project_path)
    if error: return f"Error committing files: {error}"
    print(f"... Committed with message: '{commit_message}'")

    print(f"\nStep 3: Pushing to remote branch '{current_branch}'...")
    push_command = f"git push origin {current_branch}"
    _, error = run_command(push_command, cwd=project_path)
    if error: return f"Error pushing to remote: {error}"
    print("... Done.")

    return f"\n✅ Success! Your work on '{nickname}' has been saved."
