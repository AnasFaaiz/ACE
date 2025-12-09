import os
import json
import requests
import subprocess
from dotenv import load_dotenv

ACE_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

dotenv_path = os.path.join(ACE_ROOT_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECTS_FILE = os.path.join(ACE_ROOT_DIR, "projects.json")

def get_remote_url(repo_name):
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
            return None, "NOT_FOUND"
        return None, f"An API error occurred: {e.response.text}"

def create_github_repo(repo_name, is_private):
    """Creates a new repository on GitHub via the API."""
    api_url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

    data = {
        "name": repo_name,
        "private": is_private,
        "description": f"Repository for the {repo_name} project, created by A.C.E."
    }

    print(f"Creating new {'private' if is_private else 'public'} repository on GitHub...")

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data.get("clone_url"), None
    except requests.exceptions.HTTPError as e:
        return None, f"Failed to create GitHub repository. API error: {e.response.text}"


def register_project(project_path):
    """
    Scans the specified directory path and registers it as a project with A.C.E.
    """
    local_path = os.path.abspath(project_path)
    
    if not os.path.isdir(local_path):
        return f"Error: The path '{local_path}' does not exist or is not a directory."
        
    project_nickname = os.path.basename(local_path)
    
    print(f"Scanning project: '{project_nickname}' at path: {local_path}")
    
    print("Querying GitHub for remote repository URL...")
    remote_url, error = get_remote_url(project_nickname)
    
    if error == "NOT_FOUND":
        print(f"Repository '{project_nickname}' not found on your GitHub account.")

        should_create = input("Would you like to create a new repository on GitHub with this name? [y/n] ").lower().strip()

        if should_create in ['y', 'yes', '']:
            visibility = input("Should the repository be private? [y/n] ").lower().strip()
            is_private = visibility in ['y', 'yes']

            remote_url, error = create_github_repo(project_nickname, is_private)

            if error:
                return f"Could not create repository: {error}"

            print(f" Successfully created new repository:{remote_url}")

            print("Linking local project to new remote repository..")

            is_git_repo = os.path.isdir(os.path.join(local_path, '.git'))

            if not is_git_repo:
                subprocess.run(['git', 'init'], cwd=local_path, capture_output=True)
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=local_path, capture_output=True)
            print("..Done")

        else:
            return "Registration cancelled by user."
    elif error:
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

def load_projects():
    """Returns the projects.json content as a dictionary."""
    if not os.path.exists(PROJECTS_FILE):
        return {}

    try:
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

