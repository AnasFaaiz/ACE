#!/usr/bin/env python3
import sys 
import os
from importlib.metadata import version, PackageNotFoundError

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

import argparse

try:
    __version__ = version("ace-cli")
except PackageNotFoundError:
    __version__ = "dev"

def handle_shell_init(args):
    from src import shell
    target = args.shell or shell.detect_shell()

    if args.install:
        rc, action = shell.install(target)
        print(f"acego {action} in {rc}")
        print(f"Run: source {rc}")
    else:
        print(shell.snippet(target))
        
# Command dispatch handlers (lazy loading)

def handle_project(args):
    from src.features import project_manager, project_scaffolder
    if args.action == 'register':
        print(project_manager.register_project(args.path))
    elif args.action == 'list':
        if args.plain:
            print("\n".join(project_manager.load_projects()))
        else:
            print(project_manager.list_registered_projects())
    elif args.action == 'go':
        project_path = project_manager.get_navigation_command(args.nickname)
        print(project_path)
    elif args.action == 'create':
        template = input("Template (react, nextjs, vite, python): ")
        default_dir = os.path.expanduser("~/projects/")
        loc = input(f"Where should I create it? (Enter = {default_dir}): ").strip()
        location = loc if loc else default_dir
        os.makedirs(location, exist_ok = True)
        print(project_scaffolder.create_project(args.name, template, location))


def handle_news(args):
    from src.features import news_hub
    headlines = news_hub.get_news(
        source_name=args.source, 
        limit=args.limit,
        method=args.method,
    )
    print(f"\n-- Latest from {args.source.title()} ---")
    for h in headlines:
        print(h)
    print("-------------------------------------")

def handle_save(args):
    from src.features import vanguard
    print(vanguard.save_workflow(args.nickname))

def handle_overview(args):
    from src.features import vanguard
    print(vanguard.generate_git_overview())

def handle_dashboard(args):
    from src.features import dashboard_manager
    if args.action == 'start':
        dashboard_manager.start_dashboard()

def handle_schedule(args):
    from src.features import task_scheduler
    if args.action == 'add':
        print(task_scheduler.add_scheduled_job(args.time_string, args.command_string))
    elif args.action == 'list':
        jobs = task_scheduler.list_scheduled_jobs()
        if isinstance(jobs, str):
            print(jobs)
        else:
            print("----- A.C.E. Scheduled Tasks ----")
            for job in jobs:
                print(f"ID: {job['id']} | Rule: {job['time_string']} | Command: {job['command']}")
            print("--------------------------------------------------")
    elif args.action == 'remove':
        print(task_scheduler.remove_scheduled_job(args.job_id))

def handle_scheduler(args):
    from src.features import task_scheduler
    if args.action == 'start':
        task_scheduler.start_scheduler()

def handle_backup(args):
    from src.features import project_manager, backup_manager
    projects = project_manager.load_projects()

    if args.nickname:
        info = projects.get(args.nickname)
        if not info:
            print(f"[Error] Project '{args.nickname}' not found!")
            return
        path = info.get("local_path")
        print(backup_manager.backup_single_project(args.nickname, path))
    else:
        print(backup_manager.backup_all_projects())

def handle_tui(args):
    from src.tui.app import AceTUI 
    app = AceTUI()
    app.run()

# Main ENtry & Parser 
def main():
    parser = argparse.ArgumentParser(description="A.C.E. - Your Personal AI Deeveloper Assistant.")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)


    # -------------- Project Commands ------------------------ 
    project_parser = subparsers.add_parser('project', help='Manage your registered projects')
    project_parser.set_defaults(func=handle_project)
    project_actions = project_parser.add_subparsers(dest='action', metavar='{regiser, list, create}', required=True)

    # -------------- Register Project
    register_parser = project_actions.add_parser('register', help='Register a project by path')
    register_parser.add_argument('path', type=str)

    # ---------------- List Projects 
    list_parser = project_actions.add_parser('list', help='List all registered projects')
    list_parser.add_argument('--plain', action='store_true', help=argparse.SUPPRESS)
    # --------------- Navigate project 
    go_parser = project_actions.add_parser('go')
    go_parser.add_argument('nickname', type=str)

    # ---------------- Create Project 
    create_parser = project_actions.add_parser('create', help='Create project using our templates')
    create_parser.add_argument('name', type=str)

    # -------------------- News Command 
    news_parser = subparsers.add_parser('news', help='Fetch the Latest news from sources')
    news_parser.set_defaults(func=handle_news)
    news_parser.add_argument('--source', type=str, default='hackernews')
    news_parser.add_argument('--limit', type=int, default=7)
    news_parser.add_argument('--method', type=str, default='rss', choices=['rss', 'api', 'scrape', 'all'], help="Choose news fetch type")

    # ---------------- Save Command 
    git_parser = subparsers.add_parser('save', help='The vanguard: Save your project')
    git_parser.set_defaults(func=handle_save)
    git_parser.add_argument('nickname', type=str)

    # ------------------ OverView Command
    overview_parser = subparsers.add_parser('overview', help='Show High level GIT overview for all projects')
    overview_parser.set_defaults(func=handle_overview)

    # ----------------- Dashboard Command 
    dashboard_parser = subparsers.add_parser('dashboard', help='Control tmux dashboard')
    dashboard_parser.set_defaults(func=handle_dashboard)
    dashboard_parser.add_argument('action', choices=['start'])

    # --------------- Scheduler command 
    schedule_parser = subparsers.add_parser('schedule', help='Manage A.C.E. schedules')
    schedule_parser.set_defaults(func=handle_schedule)
    schedule_actions = schedule_parser.add_subparsers(dest='action', required=True)

    add_job = schedule_actions.add_parser('add', help='Add a scheduled task')
    add_job.add_argument('time_string', type=str)
    add_job.add_argument('command_string', type=str)

    schedule_actions.add_parser('list', help='list all tasks')

    remove_job = schedule_actions.add_parser('remove', help='Remove the scheduled task')
    remove_job.add_argument('job_id', type=int)

    # --------------- Scheduler Watcher 
    scheduler_watcher_parser = subparsers.add_parser('scheduler', help='Start the scheduler watcher')
    scheduler_watcher_parser.set_defaults(func=handle_scheduler)
    scheduler_watcher_parser.add_argument('action', choices=['start'])

    # ------------------ Backup Command 
    backup_parser = subparsers.add_parser("backup", help="Backup one or all projects")
    backup_parser.set_defaults(func=handle_backup)
    backup_parser.add_argument("nickname", nargs="?", help="Specific project to backup")

    # ---------------- TUI Command 
    tui_parser = subparsers.add_parser('tui', help='Launch A.C.E. TUI Dashboard')
    tui_parser.set_defaults(func=handle_tui)

    # ---------------- acego function
    
    shell_parser = subparsers.add_parser('shell-init', help='Set up the acego shell function')
    shell_parser.set_defaults(func=handle_shell_init)
    shell_parser.add_argument('--shell', default=None, choices=['bash', 'zsh', 'fish'])
    shell_parser.add_argument('--install', action='store_true',
                          help='Write the function into your shell rc file')
    # Parse arguments 
    args = parser.parse_args()

    # Route execution 
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.error(f"no handler wired for '{args.command}'")

if __name__ == "__main__":
    main()
