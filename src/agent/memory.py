# src/agent/memory.py
from collections import deque
from typing import Optional, Dict


class AgentMemory:
    def __init__(self, max_history: int = 5):
        self.last_intent: Optional[str] = None
        self.last_command: Optional[str] = None
        self.working_context: Optional[str] = None
        self.recent_intents = deque(maxlen=max_history)

    def record(self, intent: str, command: str, context: str):
        self.last_intent = intent
        self.last_command = command
        self.working_context = context
        self.recent_intents.append(intent)

    def summary(self) -> Dict:
        return {
            "last_intent": self.last_intent,
            "last_command": self.last_command,
            "working_context": self.working_context,
            "recent_intents": list(self.recent_intents),
        }


agent_memory = AgentMemory()
