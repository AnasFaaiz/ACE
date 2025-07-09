#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

import argparse
# We import the entire project_manager module to access all its functions.
from src.features import project_manager
from src.features import news_hub
from src.features import project_scaffolder

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

    news_parser = subparsers.add_parser('news', help='Fetch the latest tech news.')

    # Add an option argument '--source'.
    news_parser.add_argument(
        '--source',
        type=str,
        default='hackernews',
        help='The news source to fetch from (e.g., hackernews, techcrunch).'
    )
    # Add an optionalargument '--limit'.
    news_parser.add_argument(
        '--limit',
        type=int,
        default=7,
        help='The number of arcticles to display.'
    )

    # New command: 'project create'
    create_parser = project_actions.add_parser('create', help='create a new project using a template.')
    create_parser.add_argument('name', type=str, help='The name of new project.')


    # This line reads all the arguments that were typed in the terminal.
    args = parser.parse_args()

    # --- Logic to call the correct function ---
    
    if args.command == 'project':
        if args.action == 'create':
            # Interactive part of workflow
            template = input("What kind of project is this? (e.g., react, nextjs, vite, python): ")

            default_project_path = os.path.expanduser('~/Documents/0-Projects')

            location_prompt = f"Where should I create this project? (Press Enter for default: {default_project_path}): "
            location_input = input(location_prompt)

            if not location_input:
                final_location = default_project_path
            else:
                final_location = os.path.expanduser(location_input)

            os.makedirs(final_location, exist_ok=True)

            result = project_scaffolder.create_project(args.name, template, final_location)
            print(result)


        elif args.action == 'register':
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
    # News logic        
    elif args.command == 'news':
        # Call the get_news function from our news_hub.
        headlines = news_hub.get_news(source_name=args.source, limit=args.limit)

        print(f"\n--- Latest from {args.source.title()} ---")

        # Loop through headlines & print each.
        for headline in headlines:
            print(headline)
        print("------------------------------")

# This standard Python line ensures that the main() function is called only when the script is executed.
if __name__ == "__main__":
    main()

