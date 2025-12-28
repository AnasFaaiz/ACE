#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

import argparse
from src.features import project_manager
from src.features import news_hub
from src.features import project_scaffolder
from src.features import vanguard
from src.features import task_scheduler
from src.features import dashboard_manager
from src.features import backup_manager


def main():
    parser = argparse.ArgumentParser(description="A.C.E. - Your Personal AI Developer Assistant.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # ---------------- PROJECT COMMAND ----------------
    project_parser = subparsers.add_parser('project', help='Manage your registered projects.')
    project_actions = project_parser.add_subparsers(dest='action', help='Project actions', required=True)

    # Register project
    register_parser = project_actions.add_parser('register', help='Register a project by path.')
    register_parser.add_argument('path', type=str)

    # List projects
    project_actions.add_parser('list', help='List all registered projects.')

    # Navigate to project
    go_parser = project_actions.add_parser('go', help="Prints the project's path so you can cd into it.")
    go_parser.add_argument('nickname', type=str)

    # Create project
    create_parser = project_actions.add_parser('create', help='Create a new project from a template.')
    create_parser.add_argument('name', type=str)

    # ---------------- NEWS COMMAND ----------------
    news_parser = subparsers.add_parser('news', help='Fetch the latest tech news.')
    news_parser.add_argument('--source', type=str, default='hackernews')
    news_parser.add_argument('--limit', type=int, default=7)
    news_parser.add_argument(
        '--method',
        type=str,
        default='rss',
        choices=['rss', 'api', 'scrape', 'all'],
        help="Choose news fetch type"
    )

    # ---------------- SAVE COMMAND ----------------
    git_parser = subparsers.add_parser('save', help='The Vanguard: Save your project work.')
    git_parser.add_argument('nickname', type=str)

    # ---------------- OVERVIEW COMMAND ----------------
    subparsers.add_parser('overview', help='Show high-level GIT overview for all projects.')

    # ---------------- DASHBOARD COMMAND ----------------
    dashboard_parser = subparsers.add_parser('dashboard', help='Control the tmux dashboard.')
    dashboard_parser.add_argument('action', choices=['start'])

    # ---------------- SCHEDULER COMMAND ----------------
    schedule_parser = subparsers.add_parser('schedule', help='Manage ACE scheduler.')
    schedule_actions = schedule_parser.add_subparsers(dest='action', required=True)

    add_job = schedule_actions.add_parser('add', help='Add a scheduled task.')
    add_job.add_argument('time_string', type=str)
    add_job.add_argument('command_string', type=str)

    schedule_actions.add_parser('list', help='List all tasks.')

    remove_job = schedule_actions.add_parser('remove', help='Remove a scheduled task.')
    remove_job.add_argument('job_id', type=int)

    scheduler_parser = subparsers.add_parser('scheduler', help='Start the scheduler watcher.')
    scheduler_parser.add_argument('action', choices=['start'])

    # ---------------- BACKUP COMMAND ----------------
    backup_parser = subparsers.add_parser("backup", help="Backup one or all projects.")
    backup_parser.add_argument("nickname", nargs="?", help="Specific project to backup")

    # Parse arguments
    args = parser.parse_args()

    # ---------------- PROJECT LOGIC ----------------
    if args.command == 'project':
        if args.action == 'register':
            print(project_manager.register_project(args.path))

        elif args.action == 'list':
            print(project_manager.list_registered_projects())

        elif args.action == 'go':
            project_path = project_manager.get_navigation_command(args.nickname)
            print(project_path)

        elif args.action == 'create':
            template = input("Template (react, nextjs, vite, python): ")
            default_dir = os.path.expanduser("~/Documents/0-Projects")
            loc = input(f"Where should I create it? (Enter = {default_dir}): ").strip()
            location = loc if loc else default_dir
            os.makedirs(location, exist_ok=True)
            print(project_scaffolder.create_project(args.name, template, location))

    # ---------------- NEWS LOGIC ----------------
    elif args.command == 'news':
        headlines = news_hub.get_news(
            source_name=args.source,
            limit=args.limit,
            # method=args.method
        )
        print(f"\n--- Latest from {args.source.title()} ---")
        for h in headlines:
            print(h)
        print("--------------------------------")

    # ---------------- SAVE LOGIC ----------------
    elif args.command == 'save':
        print(vanguard.save_workflow(args.nickname))

    # ---------------- OVERVIEW LOGIC ----------------
    elif args.command == 'overview':
        print(vanguard.generate_git_overview())

    # ---------------- DASHBOARD LOGIC ----------------
    elif args.command == 'dashboard':
        if args.action == 'start':
            dashboard_manager.start_dashboard()

    # ---------------- SCHEDULE LOGIC ----------------
    elif args.command == 'schedule':
        if args.action == 'add':
            print(task_scheduler.add_scheduled_job(args.time_string, args.command_string))
        elif args.action == 'list':
            jobs = task_scheduler.list_scheduled_jobs()
            if isinstance(jobs, str):
                print(jobs)
            else:
                print("--- A.C.E. Scheduled Tasks ---")
                for job in jobs:
                    print(f"ID: {job['id']} | Rule: {job['time_string']} | Command: {job['command']}")
                print("--------------------------------")
        elif args.action == 'remove':
            print(task_scheduler.remove_scheduled_job(args.job_id))

    # ---------------- SCHEDULER WATCHER ----------------
    elif args.command == 'scheduler':
        if args.action == 'start':
            task_scheduler.start_scheduler()

    # ---------------- BACKUP LOGIC ----------------
    elif args.command == "backup":
        projects = project_manager.load_projects()

        if args.nickname:
            info = projects.get(args.nickname)

            if not info:
                print(f"[ERROR] Project '{args.nickname}' not found.")
                return

            path = info.get("local_path")
            print(backup_manager.backup_single_project(args.nickname, path))

        else:
            print(backup_manager.backup_all_projects()) 

if __name__ == "__main__":
    main()

