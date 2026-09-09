from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import analyze_with_agent
from .service import build_case

app = FastAPI(title="MAAT Universal CaseGraph", version="0.1.0")


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
