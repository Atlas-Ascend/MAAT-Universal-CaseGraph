from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent import analyze_with_agent
from .service import build_case

app = FastAPI(title="MAAT Universal CaseGraph", version="0.1.0")
WEB_DIR = Path(__file__).resolve().parents[2] / "web"


class BuildRequest(BaseModel):
    text: str = Field(min_length=1)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "system": "MAAT"}


@app.post("/build-case")
def build_case_route(request: BuildRequest) -> dict:
    return build_case(request.text).model_dump(mode="json")


@app.post("/agent-analysis")
def agent_analysis(request: BuildRequest) -> dict:
    return {"analysis": analyze_with_agent(request.text)}


@app.get("/")
def demo_ui() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
