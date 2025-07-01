
import argparse
# We import the entire project_manager module to access all its functions.
from .features import project_manager 

def main():
    """
    This is the main function that runs when you execute the script.
    It sets up the command-line interface.
    """
    # Create the main parser object for the 'ace' command.
    parser = argparse.ArgumentParser(description="A.C.E. - Your Personal AI Developer Assistant.")
    
    # This creates the main command groups (e.g., 'project', 'git').
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # --- Command Group: 'project' ---
    project_parser = subparsers.add_parser('project', help='Manage your registered projects.')
    # This creates a new layer for actions within the 'project' group (e.g., 'register', 'list', 'go').
    # This is a more organized way than your previous version.
    project_actions = project_parser.add_subparsers(dest='action', help='Project actions', required=True)

    # Action: 'register'
    # We now use the 'register_project(path)' function, so we expect a path.
    register_parser = project_actions.add_parser('register', help='Register a project by its path.')
    register_parser.add_argument('path', type=str, help='The full or relative path to the project you want to register.')
    
    # Action: 'list'
    # The 'list' action doesn't need any extra arguments.
    list_parser = project_actions.add_parser('list', help='List all registered projects.')

    # --- NEW: Action 'go' ---
    # Create a new parser specifically for the 'go' action.
    go_parser = project_actions.add_parser('go', help='Prints the \'cd\' command to navigate to a registered project.')
    # Tell the 'go' parser that it must be followed by a 'nickname' argument.
    go_parser.add_argument('nickname', type=str, help='The nickname of the project to navigate to.')

    # This line reads all the arguments that were typed in the terminal.
    args = parser.parse_args()

    # --- Logic to call the correct function ---
    
    if args.command == 'project':
        if args.action == 'register':
            # We call the register function with the path the user provided.
            result = project_manager.register_project(args.path)
            print(result)
        
        elif args.action == 'list':
            # We call the list function we created.
            result = project_manager.list_registered_projects()
            print(result)

        # --- NEW: Logic for the 'go' action ---
        elif args.action == 'go':
            # We call the new function from our project_manager skill.
            # We pass it the nickname the user typed.
            navigation_command = project_manager.get_navigation_command(args.nickname)
            # We print the result, which will be our 'cd ...' command or an error.
            print(navigation_command)

# This standard Python line ensures that the main() function is called only when the script is executed.
if __name__ == "__main__":
    main()

