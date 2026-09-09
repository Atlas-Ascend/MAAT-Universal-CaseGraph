from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from . import __version__
from .agent import AgentUnavailableError, agent_runtime_configured, analyze_with_agent
from .service import build_case

app = FastAPI(title="MAAT Universal CaseGraph", version=__version__)
WEB_DIR = Path(__file__).resolve().parents[2] / "web"


class BuildRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must contain non-whitespace content")
        return value


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-MAAT-Version"] = __version__
    return response


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "system": "MAAT", "version": __version__}


@app.get("/ready")
def ready() -> dict:
    return {
        "status": "ok",
        "core": "ready",
        "agent_runtime": "configured" if agent_runtime_configured() else "not_configured",
        "version": __version__,
    }


@app.post("/build-case")
def build_case_route(request: BuildRequest) -> dict:
    return build_case(request.text).model_dump(mode="json")


@app.post("/agent-analysis")
def agent_analysis(request: BuildRequest) -> dict:
    try:
        return {"analysis": analyze_with_agent(request.text), "provider_path": "strands/bedrock"}
    except AgentUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Model-backed analysis failed. The deterministic /build-case path remains available.",
        ) from exc


@app.get("/")
def demo_ui() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
