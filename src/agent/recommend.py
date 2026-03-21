from src.agent.commands import COMMANDS


def recommend_next(intent: str):
    """
    Simple heuristic recommendations based on last intent.
    """

    if intent == "news":
        return ["overview", "project.list"]

    if intent == "project.list":
        return ["overview", "backup"]

    if intent == "overview":
        return ["project.list", "news"]

    return []
