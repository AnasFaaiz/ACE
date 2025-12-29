#!/usr/bin/env python3
import sys
import os
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.dispatcher import run_command


def main():
    parser = argparse.ArgumentParser(
        description="A.C.E. - Your Personal AI Developer Assistant."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---------- PROJECT ----------
    project_parser = subparsers.add_parser("project")
    project_actions = project_parser.add_subparsers(dest="action", required=True)

    register = project_actions.add_parser("register")
    register.add_argument("path")

    project_actions.add_parser("list")

    go = project_actions.add_parser("go")
    go.add_argument("nickname")

    create = project_actions.add_parser("create")
    create.add_argument("name")

    # ---------- NEWS ----------
    news = subparsers.add_parser("news")
    news.add_argument("--source", default="hackernews")
    news.add_argument("--limit", type=int, default=7)
    news.add_argument(
        "--method",
        default="rss",
        choices=["rss", "api", "scrape", "all"],
    )

    # ---------- SAVE ----------
    save = subparsers.add_parser("save")
    save.add_argument("nickname")

    # ---------- OVERVIEW ----------
    subparsers.add_parser("overview")

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

    scheduler = subparsers.add_parser("scheduler")
    scheduler.add_argument("action", choices=["start"])

    # ---------- BACKUP ----------
    backup = subparsers.add_parser("backup")
    backup.add_argument("nickname", nargs="?")

    args = parser.parse_args()

    # ---------- ROUTING ----------
    if args.command == "project":
        if args.action == "register":
            output = run_command(
                "project.register",
                {"path": args.path},
            )

        elif args.action == "list":
            output = run_command("project.list", {})

        elif args.action == "go":
            output = run_command(
                "project.go",
                {"nickname": args.nickname},
            )

        elif args.action == "create":
            template = input("Template (react, nextjs, vite, python): ")
            default_dir = os.path.expanduser("~/Documents/0-Projects")
            loc = input(
                f"Where should I create it? (Enter = {default_dir}): "
            ).strip()
            location = loc if loc else default_dir

            output = run_command(
                "project.create",
                {
                    "name": args.name,
                    "template": template,
                    "location": location,
                },
            )

    elif args.command == "news":
        output = run_command(
            "news",
            {
                "source": args.source,
                "limit": args.limit,
                "method": args.method,
            },
        )

        print(f"\n--- Latest from {args.source.title()} ---")
        for h in output:
            print(h)
        print("--------------------------------")
        return

    elif args.command == "save":
        output = run_command(
            "save",
            {"nickname": args.nickname},
        )

    elif args.command == "overview":
        output = run_command("overview", {})

    elif args.command == "dashboard":
        output = run_command("dashboard.start", {})

    elif args.command == "schedule":
        if args.action == "add":
            output = run_command(
                "schedule.add",
                {
                    "time_string": args.time_string,
                    "command_string": args.command_string,
                },
            )

        elif args.action == "list":
            output = run_command("schedule.list", {})
            if isinstance(output, list):
                print("--- A.C.E. Scheduled Tasks ---")
                for job in output:
                    print(
                        f"ID: {job['id']} | Rule: {job['time_string']} | Command: {job['command']}"
                    )
                print("--------------------------------")
                return

        elif args.action == "remove":
            output = run_command(
                "schedule.remove",
                {"job_id": args.job_id},
            )

    elif args.command == "scheduler":
        output = run_command("scheduler.start", {})

    elif args.command == "backup":
        output = run_command(
            "backup",
            {"nickname": args.nickname},
        )

    print(output)


if __name__ == "__main__":
    main()

