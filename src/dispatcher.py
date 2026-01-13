# src/dispatcher.py
import os
from src.agent.commands import COMMANDS
from src.agent.intent import interpret_intent
from src.agent.memory import agent_memory
from src.features import (
    project_manager,
    project_scaffolder,
    task_scheduler,
    dashboard_manager,
    backup_manager,
)

ACE_MODE = os.getenv("ACE_MODE", "cli")


# INTERNAL EXECUTOR
def _execute_registry_command(command: str, args: dict):
    cmd = COMMANDS.get(command)

    if not cmd:
        return None

    result = cmd["handler"](args)

    if result is None:
        return {"message": "No data available."}

    if isinstance(result, list):
        return {
            "type": "list",
            "items": result,
        }

    if isinstance(result, dict):
        return result

    return {"message": str(result)}


def _execute_system_command(command: str, args: dict):
    if command == "project.register":
        return project_manager.register_project(args["path"])

    # elif command == "project.list":
    #     return project_manager.list_registered_projects()

    elif command == "project.go":
        return project_manager.get_navigation_command(args["nickname"])

    elif command == "project.create":
        name = args["name"]
        template = args["template"]
        location = args["location"]
        os.makedirs(location, exist_ok=True)
        return project_scaffolder.create_project(name, template, location)

    # elif command == "news":
    #     return news_hub.get_news(
    #         source_name=args.get("source", "hackernews"),
    #         limit=args.get("limit", 7),
    #         method=args.get("method", "rss"),
    #     )

    # elif command == "overview":
    #     return vanguard.generate_git_overview()
    #
    # elif command == "memory":
    #     memory = agent_memory.summary()
    #
    #     if not memory["last_intent"]:
    #         return {
    #             "message": "I don't have enough context yet.",
    #             "hint": "Try running a command first.",
    #         }
    #     return {
    #         "message": f"you were last working on: {memory['working_context']}",
    #         "last_command": memory["last_command"],
    #         "recent_intents": memory["recent_intents"],
    #     }
    #
    # elif command == "help":
    #     return {
    #         "commands": sorted(WEB_ALLOWED_COMMANDS),
    #         "note": "Natural language supported in web mode",
    #         "examples": [
    #             "latest tech news",
    #             "what am I working on",
    #             "list my projects",
    #         ],
    #     }

    elif command == "dashboard.start":
        dashboard_manager.start_dashboard()
        return "Dashboard started"

    elif command == "schedule.add":
        return task_scheduler.add_scheduled_job(
            args["time_string"],
            args["command_string"],
        )

    elif command == "schedule.list":
        return task_scheduler.list_scheduled_jobs()

    elif command == "schedule.remove":
        return task_scheduler.remove_scheduled_job(args["job_id"])

    elif command == "backup":
        projects = project_manager.load_projects()
        nickname = args.get("nickname")

        if nickname:
            info = projects.get(nickname)
            if not info:
                return f"[ERROR] Project '{nickname}' not found."
            return backup_manager.backup_single_project(
                nickname,
                info["local_path"],
            )

        return backup_manager.backup_all_projects()

    return f"[ERROR] Unknown command: {command}"


# MAIN DISPATCHER
def run_command(command: str, args: dict):
    """
    Central ACE dispatcher.
    Used by CLI, API, Web, DreamFlow.
    """

    if ACE_MODE == "web" and command not in COMMANDS:
        analysis = interpret_intent(command)

        if analysis["intent"] and analysis["intent"] in COMMANDS:
            agent_memory.record(
                intent=analysis["intent"],
                command=f"ace {analysis['intent'].replace('.', ' ')}",
                context=f"User intent: {analysis['intent']}",
            )

            return {
                "agent": "ACE",
                "message": analysis["message"],
                "interpreted_as": analysis["intent"],
                "confidence": analysis["confidence"],
                "suggestion": f"ace {analysis['intent'].replace('.', ' ')}",
                "result": _execute_registry_command(analysis["intent"], {}),
            }

        return {
            "agent": "ACE",
            "error": "I couldn't understand that request.",
            "examples": [
                "latest tech news",
                "what am I working on",
                "list my projects",
                "help",
            ],
        }

    # ---------- WEB SAFETY ALLOWLIST ----------
    if command in COMMANDS:
        if ACE_MODE == "web" and not COMMANDS[command]["web_safe"]:
            return {"error": f"Command '{command}' not allowed in web mode."}

        return _execute_registry_command(command, args)

    result = _execute_system_command(command, args)
    if result is not None:
        return result

    return f"[ERROR] Unknown command: {command}"
