#!/usr/bin/env python3
import sys
import os
import argparse

# --- ensure project root in path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from dispatcher import run_command


def main():
    parser = argparse.ArgumentParser(
        description="A.C.E. – Your Personal AI Developer Assistant"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---------- PROJECT ----------
    project = subparsers.add_parser("project")
    project_actions = project.add_subparsers(dest="action", required=True)

    register = project_actions.add_parser("register")
    register.add_argument("path")

    project_actions.add_parser("list")

    go = project_actions.add_parser("go")
    go.add_argument("nickname")

    create = project_actions.add_parser("create")
    create.add_argument("name")
    create.add_argument("--template", default="python")
    create.add_argument(
        "--location", default=os.path.expanduser("~/Documents/0-Projects")
    )

    # ---------- NEWS ----------
    news = subparsers.add_parser("news")
    news.add_argument("--source", default="hackernews")
    news.add_argument("--limit", type=int, default=7)
    news.add_argument("--method", default="rss")

    # ---------- OVERVIEW ----------
    subparsers.add_parser("overview")

    # ---------- HELP ----------
    subparsers.add_parser("help")

    # ---------- DASHBOARD ----------
    dashboard = subparsers.add_parser("dashboard")
    dashboard.add_argument("action", choices=["start"])

    # ---------- SCHEDULE ----------
    schedule = subparsers.add_parser("schedule")
    schedule_actions = schedule.add_subparsers(dest="action", required=True)

    add = schedule_actions.add_parser("add")
    add.add_argument("time_string")
    add.add_argument("command_string")

    schedule_actions.add_parser("list")

    remove = schedule_actions.add_parser("remove")
    remove.add_argument("job_id", type=int)

    # ---------- BACKUP ----------
    backup = subparsers.add_parser("backup")
    backup.add_argument("nickname", nargs="?")

    args = parser.parse_args()

    # ---------- BUILD COMMAND STRING ----------
    command = args.command
    if hasattr(args, "action") and args.action:
        command = f"{args.command}.{args.action}"

    # ---------- BUILD ARGUMENT DICT ----------
    args_dict = vars(args).copy()
    args_dict.pop("command", None)
    args_dict.pop("action", None)

    # ---------- EXECUTE ----------
    output = run_command(command, args_dict)
    print(output)


if __name__ == "__main__":
    main()
