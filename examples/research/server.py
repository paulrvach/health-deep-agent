#!/usr/bin/env python

"""LangServe server for the health agent."""

import os
from pathlib import Path
from typing import Any, Dict

# Load environment variables from .env file before importing the agent
from dotenv import load_dotenv

# Load .env file from the same directory as this script
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel

from health_agent import agent

app = FastAPI(
    title="Health Agent API",
    description="API for health and wellness coaching agent",
    version="1.0.0",
)

# Define input/output schemas for LangGraph agent
class AgentInput(BaseModel):
    """Input schema for the health agent."""

    messages: list[Dict[str, Any]]


class AgentOutput(BaseModel):
    """Output schema for the health agent."""

    messages: list[Dict[str, Any]]


# Wrap the agent with explicit types to avoid schema inference issues
typed_agent = agent.with_types(
    input_type=AgentInput,
    output_type=AgentOutput,
)

# Add the agent routes
# This automatically creates:
# - POST /health-agent/invoke - for synchronous invocation
# - POST /health-agent/stream - for streaming responses
# - POST /health-agent/batch - for batch processing
# - GET /docs - API documentation
add_routes(app, typed_agent, path="/health-agent")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

