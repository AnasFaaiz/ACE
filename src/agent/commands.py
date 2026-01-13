"""
ACE Command Registry
--------------------
Single source of truth for:
- what commands exist
- how they execute
- whether they are web-safe
- how they are described (help / UI / NLP)
"""

from typing import Dict, Any

from src.features import (
    project_manager,
    vanguard,
    news_hub,
)
from src.agent.memory import agent_memory

CommandDef = Dict[str, Any]

COMMANDS: Dict[str, CommandDef] = {
    "news": {
        "handler": lambda args: news_hub.get_news(
            source_name=args.get("source", "hackernews") if args else "hackernews",
            limit=args.get("limit", 7) if args else 7,
            method=args.get("method", "rss") if args else "rss",
        ),
        "description": "Show latest tech news",
        "web_safe": True,
        "examples": [
            "latest tech news",
            "show me the news",
            "tech headlines",
        ],
    },
    "overview": {
        "handler": lambda _args: vanguard.generate_git_overview(),
        "description": "Show what you are currently working on",
        "web_safe": True,
        "examples": [
            "what am I working on",
            "project status",
            "current work",
        ],
    },
    "project.list": {
        "handler": lambda _args: project_manager.list_registered_projects(),
        "description": "List all registered projects",
        "web_safe": True,
        "examples": [
            "list my projects",
            "show my projects",
            "what projects do I have",
        ],
    },
    "help": {
        "handler": lambda _args: {
            "commands": sorted(COMMANDS.keys()),
            "usage": "You can type commands or natural language",
            "examples": [
                "latest tech news",
                "what am I working on",
                "list my projects",
            ],
        },
        "description": "Show available commands",
        "web_safe": True,
        "examples": [
            "help",
            "what can you do",
            "available commands",
        ],
    },
    "memory": {
        "handler": lambda _args: agent_memory.summary(),
        "description": "Show what you were last working on",
        "web_safe": True,
        "examples": [
            "what was I doing",
            "memory",
            "last command",
        ],
    },
}
