"""
Main application file for the Agent Discovery API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import time
import os
from typing import List, Dict, Any, Optional

# Import modules
from agent_discovery.db.agent_repository import get_agents, get_agent_by_id
from agent_discovery.matching.engine import match_agents
from agent_discovery.utils.logging import log_query

# Create FastAPI app
app = FastAPI(
    title="Agent Discovery API",
    description="API for discovering and matching agents",
    version="0.1.0",
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="agent_discovery/static"), name="static")


class QueryRequest(BaseModel):
    query: str


class AgentResponse(BaseModel):
    agents: List[Dict[str, Any]]


class AgentQueryResponse(BaseModel):
    agents: List[Dict[str, Any]]
    executionTime: str


class SingleAgentResponse(BaseModel):
    agent: Dict[str, Any]


@app.get("/api/agents", response_model=AgentResponse)
async def agents_route():
    """
    Returns all available agents
    """
    try:
        agents = get_agents()
        return {"agents": agents}
    except Exception as e:
        print(f"Error fetching agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch agents")


@app.post("/api/agents/queries", response_model=AgentQueryResponse)
async def agent_queries_route(request: QueryRequest):
    """
    Matches agents to a query
    """
    try:
        query = request.query

        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        start_time = time.time()

        # Get all available agents
        available_agents = get_agents()

        # Match agents to the query
        matched_agents = match_agents(query, available_agents)

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Log the query
        log_query(query, matched_agents, execution_time)


        return {"agents": matched_agents, "executionTime": f"{execution_time:.2f}ms"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Failed to process query")


@app.get("/api/agents/{agent_id}", response_model=SingleAgentResponse)
async def agent_by_id_route(agent_id: str):
    """
    Returns a specific agent by ID
    """
    try:
        agent = get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"agent": agent}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch agent")


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the root page
    """
    with open("agent_discovery/static/index.html", "r") as file:
        return HTMLResponse(content=file.read())


@app.get("/query", response_class=HTMLResponse)
async def query_page():
    """
    Serves the query page
    """
    with open("agent_discovery/static/query.html", "r") as file:
        return HTMLResponse(content=file.read())


@app.post("/api/recommendations")
async def recommendations(request: QueryRequest):
    """
    Recommendations endpoint
    """
    return JSONResponse(
        status_code=404,
        content={"detail": "Recommendations endpoint not implemented"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent_discovery.main:app", host="0.0.0.0", port=8000, reload=True)
