from fastapi import FastAPI
from pydantic import BaseModel
from src.dispatcher import run_command

app = FastAPI(title="ACE Agent API")


class RunRequest(BaseModel):
    command: str
    args: dict = {}


@app.post("/run")
def run(req: RunRequest):
    output = run_command(req.command, req.args)
    return {"Output": output}
