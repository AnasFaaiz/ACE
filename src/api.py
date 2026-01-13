from fastapi import FastAPI
from pydantic import BaseModel
from src.dispatcher import run_command
from src.dispatcher import ACE_MODE
from src.agent.commands import COMMANDS
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

app = FastAPI(title="ACE Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    command: str
    args: Dict[str, Any] = {}


@app.post("/run")
def run(req: RunRequest):
    output = run_command(req.command, req.args)
    return {"Output": output}


@app.get("/capabilities")
def capabilities():
    if ACE_MODE == "web":
        return {
            "mode": "web",
            "allowed_commands": sorted(
                name for name, cmd in COMMANDS.items() if cmd.get("web_safe")
            ),
        }

    return {
        "mode": "cli",
        "allowed_commands": "all",
    }
