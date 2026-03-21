# ==============================================================================
# A.C.E. SKILL: The Project Scaffolder (Vite Upgraded)
# ==============================================================================

import os
import subprocess

# --- Configuration: Define the commands for each template ---
SCAFFOLD_COMMANDS = {
    # --- CHANGE #1: Upgraded the React Template ---
    # The command for the "react" template was changed from the old 'create-react-app'
    # to the modern and much faster 'create-vite'. The '--template react' flag
    # tells Vite to set up a project specifically for React.
    "react": "npx create-vite@latest {project_name} --template react",
    
    "nextjs": "npx create-next-app@latest {project_name}",
    "vite": "npx create-vite@latest {project_name}",
    "python": "echo 'Python template coming soon!'" 
}

def create_project(project_name, template, location):
    """
    Creates a new project using an external scaffolding tool.
    """
    template = template.strip().lower()
    
    if template not in SCAFFOLD_COMMANDS:
        return f"Error: Unknown project template '{template}'. Available templates are: {list(SCAFFOLD_COMMANDS.keys())}"

    command_template = SCAFFOLD_COMMANDS[template]
    command_to_run = command_template.format(project_name=project_name)

    print(f"--- Preparing to create '{project_name}' using the '{template}' template ---")
    print(f"Location: {location}")
    print(f"Command to run: {command_to_run}\n")

    try:
        # This part for running the command remains the same.
        process = subprocess.Popen(
            command_to_run,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=location
        )

        for line in process.stdout:
            print(line, end='')

        process.wait()
        
        if process.returncode != 0:
            return f"\n❌ Error: The project creation command failed with exit code {process.returncode}."

        # --- CHANGE #2: Added Helpful "Next Steps" ---
        # Unlike create-react-app, Vite doesn't automatically install dependencies.
        # This new block creates a more helpful success message that tells the
        # user exactly what to do next.
        project_path = os.path.join(location, project_name)
        success_message = (
            f"\n✅ Success! Project '{project_name}' has been created at '{location}'.\n\n"
            f"Next steps:\n"
            f"  1. cd {project_path}\n"
            f"  2. npm install\n"
            f"  3. npm run dev"
        )
        return success_message

    except FileNotFoundError:
        return f"Error: The command '{command_to_run.split()[0]}' was not found. Please ensure it is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

