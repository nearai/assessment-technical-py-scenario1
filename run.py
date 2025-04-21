"""
Script to run the Agent Discovery API
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("agent_discovery.main:app", host="0.0.0.0", port=8000, reload=True)