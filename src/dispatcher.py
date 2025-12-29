from src.features import (
    project_manager,
    project_scaffolder,
    vanguard,
    news_hub,
    task_scheduler,
    dashboard_manager,
    backup_manager,
)
import os

ACE_MODE = os.getenv("ACE_MODE", "cli")

WEB_ALLOWED_COMMANDS = {"overview", "news", "help", "project.list"}


def run_command(command: str, args: dict):
    """
    Central ACE dispatcher.
    Used b CLI, API, Dreamflow.
    """

    if ACE_MODE == "web":
        if command not in WEB_ALLOWED_COMMANDS:
            return {"error": f"Command '{command}' is not available in web mode."}

    if command == "project.register":
        return project_manager.register_project(args["path"])

    elif command == "project.list":
        return project_manager.list_registered_projects()

    elif command == "project.go":
        return project_manager.get_navigation_command(args["nickname"])

    elif command == "project.create":
        name = args["name"]
        template = args["template"]
        location = args["location"]
        os.makedirs(location, exist_ok=True)
        return project_scaffolder.create_project(name, template, location)

    elif command == "news":
        return news_hub.get_news(
            source_name=args["source"],
            limit=args["limit"],
            method=args["method"],
        )

    elif command == "save":
        return vanguard.save_workflow(args["nickname"])

    elif command == "overview":
        return vanguard.generate_git_overview()

    elif command == "dashboard.start":
        dashboard_manager.start_dashboard()
        return "Dashboard started"

    elif command == "schedule.add":
        return task_scheduler.add_scheduled_job(
            args["time_string"], args["command_string"]
        )

    elif command == "schedule.list":
        return task_scheduler.list_scheduled_jobs()

    elif command == "schedule.remove":
        return task_scheduler.remove_scheduled_job(args["job_id"])

    elif command == "scheduler.start":
        task_scheduler.start_scheduler()
        return "Scheduler started"

    elif command == "backup":
        projects = project_manager.load_projects()
        nickname = args.get("nickname")

        if nickname:
            info = projects.get(nickname)
            if not info:
                return f"[ERROR] Project '{nickname}' not found."
            return backup_manager.backup_single_project(nickname, info["local_path"])

        return backup_manager.backup_all_projects()
    return f"[ERROR] Unkown command: {command}"
