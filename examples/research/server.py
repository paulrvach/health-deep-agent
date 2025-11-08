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

# Import agent after environment variables are loaded
try:
    from health_agent import agent
except Exception as e:
    import sys
    print(f"Error importing health_agent: {e}", file=sys.stderr)
    raise

app = FastAPI(
    title="Health Agent API",
    description="API for health and wellness coaching agent",
    version="1.0.0",
)

# Add the agent routes
# This automatically creates:
# - POST /health-agent/invoke - for synchronous invocation
# - POST /health-agent/stream - for streaming responses
# - POST /health-agent/batch - for batch processing
# - GET /docs - API documentation
# Note: We don't use with_types() here to allow direct message passing
add_routes(app, agent, path="/health-agent")


if __name__ == "__main__":
    import uvicorn

    # Cloud Run provides PORT environment variable, default to 8000 for local development
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

