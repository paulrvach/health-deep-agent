# Health Agent Server

A LangServe server for the health and wellness coaching agent with doctor and coach subagents.

## Setup

1. **Create a `.env` file** in this directory with your environment variables:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   GOOGLE_API_KEY=your_google_api_key
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=your_langsmith_project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

Run the server:
```bash
python server.py
```

The server will start on `http://0.0.0.0:8000`

## API Endpoints

Once running, the server provides:

- `POST /health-agent/invoke` - Synchronous invocation
- `POST /health-agent/stream` - Streaming responses
- `POST /health-agent/batch` - Batch processing
- `GET /docs` - Interactive API documentation (Swagger UI)

## Example Request

```bash
curl -X POST "http://localhost:8000/health-agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "What are some good exercises for lower back pain?"
      }
    ]
  }'
```

## Deploying to Google Cloud Run

### Using Dockerfile

1. **Build the Docker image**:
   ```bash
   docker build -t health-agent .
   ```

2. **Tag and push to Google Container Registry**:
   ```bash
   docker tag health-agent gcr.io/YOUR_PROJECT_ID/health-agent
   docker push gcr.io/YOUR_PROJECT_ID/health-agent
   ```

3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy health-agent \
     --image gcr.io/YOUR_PROJECT_ID/health-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars TAVILY_API_KEY=your_key,GOOGLE_API_KEY=your_key,LANGSMITH_TRACING=true,LANGSMITH_ENDPOINT=https://api.smith.langchain.com,LANGSMITH_API_KEY=your_key,LANGSMITH_PROJECT=your_project
   ```

### Using Cloud Build

1. **Create a `cloudbuild.yaml`** (optional, for automated builds)

2. **Deploy**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/health-agent
   gcloud run deploy health-agent \
     --image gcr.io/YOUR_PROJECT_ID/health-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars TAVILY_API_KEY=your_key,GOOGLE_API_KEY=your_key,LANGSMITH_TRACING=true,LANGSMITH_ENDPOINT=https://api.smith.langchain.com,LANGSMITH_API_KEY=your_key,LANGSMITH_PROJECT=your_project
   ```

## Environment Variables

Make sure to set all required environment variables in Cloud Run:
- `TAVILY_API_KEY` - Your Tavily API key for web search
- `GOOGLE_API_KEY` - Your Google API key for Gemini model
- `LANGSMITH_TRACING` - Enable/disable LangSmith tracing
- `LANGSMITH_ENDPOINT` - LangSmith API endpoint
- `LANGSMITH_API_KEY` - Your LangSmith API key
- `LANGSMITH_PROJECT` - Your LangSmith project name

## Notes

- The server uses Python 3.12 (as specified in the Dockerfile)
- The agent uses Gemini 2.0 Flash model
- The server runs on port 8000 by default
- Make sure to set appropriate memory and CPU limits in Cloud Run based on your usage

