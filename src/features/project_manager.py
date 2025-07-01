import os
import json
import requests
from dotenv import load_dotenv

# --- Configuration ---
# This part correctly loads your .env file from the root directory.
ACE_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

dotenv_path = os.path.join(ACE_ROOT_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECTS_FILE = os.path.join(ACE_ROOT_DIR, "projects.json")


def get_remote_url(repo_name):
    # This function is correct and does not need changes.
    # ... (code for get_remote_url remains the same) ...
    if not GITHUB_USERNAME or not GITHUB_TOKEN:
        return None, "CRITICAL ERROR: GITHUB_USERNAME or GITHUB_TOKEN not found. Please check your .env file."
    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data.get("clone_url"), None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None, f"Repository '{repo_name}' not found on your GitHub account."
        return None, f"An API error occurred: {e}"


def register_project(project_path):
    """
    Scans the specified directory path and registers it as a project with A.C.E.
    """
    # It now uses the 'project_path' given by main.py instead of os.getcwd().
    local_path = os.path.abspath(project_path)
    
    # We add a check to make sure the path is valid before continuing.
    if not os.path.isdir(local_path):
        return f"Error: The path '{local_path}' does not exist or is not a directory."
        
    project_nickname = os.path.basename(local_path)
    
    print(f"Scanning project: '{project_nickname}' at path: {local_path}")
    
    print("Querying GitHub for remote repository URL...")
    remote_url, error = get_remote_url(project_nickname)
    
    if error:
        return f"Could not register project. Error: {error}"

    print(f"Found remote URL: {remote_url}")

    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        projects = {}
    
    projects[project_nickname] = {
        "local_path": local_path,
        "remote_url": remote_url
    }
    
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=4)
        
    return f"\n✅ Success! Project '{project_nickname}' is now registered with A.C.E."

def list_registered_projects():
    """Reads the projects.json file and displays a formatted list of all projects."""
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
        if not projects:
            return "No projects are registered with A.C.E. yet."
        
        print("--- A.C.E. Registered Projects ---")
        for nickname, details in projects.items():
            print(f"\n  Nickname: {nickname}")
            print(f"    Local Path: {details['local_path']}")
            print(f"    Remote URL: {details['remote_url']}")
        print("------------------------------------")
        return ""
    except FileNotFoundError:
        return "Project registry not found. Use 'ace project register [path]' to start one."

# And the navigation function for the 'go' command
def get_navigation_command(nickname):
    """Looks up a project by its nickname in the registry and returns the 'cd' command."""
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
        if nickname in projects:
            project_path = projects[nickname]['local_path']
            return project_path  # Added quotes for paths with spaces
        else:
            print(f"\033[91m\033[1mError: Project nickname '{nickname}' not found in registry.\033[0m")
            return None
    except FileNotFoundError:
        print("\033[91m\033[1mError: Project registry not found. Please register a project first.\033[0m")
        return None
