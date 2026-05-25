
# Agentic AI API

Production-grade multi-agent orchestration platform with:
- LangGraph workflows
- Streaming APIs
- Provider abstraction
- Durable execution
- Memory layer
- Observability
- Multi-agent orchestration

# Stack
- FastAPI
- LangGraph
- Redis
- PostgreSQL
- OpenTelemetry
- Docker

# Quick start

## Git Clone

````shell
git clone agentic-ai-api
cd agentic-ai-api
````

## Setup environment variables
- Copy the example environment file and update it as needed
- Add **GEMINI_API_KEY** & **REDIS_URL** if you want generative answers

````shell
cp .env.example .env
````

## Create and activate virtual environment

````shell
python3 -m venv .venv
source .venv/bin/activate
````

## Install dependencies

````shell
pip3 install -r requirements.txt
````

## Run docker

````shell
docker run -p 6379:6379 redis
````

## Run the API

```shell
uvicorn app.main:app --reload
```

## Run the CURL

```shell
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/chat \
-H "Content-Type: application/json" \
-d '{ "session_id": "anshul","title":"Sample","message":"My name is anshul"}'

curl -X POST http://localhost:8000/api/v1/chat \
-H "Content-Type: application/json" \
-d '{ "session_id": "anshul","title":"Sample","message":"Whats my name?"}'

curl -N -X POST http://localhost:8000/api/v1/chat/stream \
-H "Content-Type: application/json" \
-d '{
  "session_id": "user-1",
  "message": "Explain LangGraph"
}'
```

## Run eval

```shell
python -m app.evaluation.run_eval
```

# What to track in AI-Observability?

- How long did planner node take?
- How many retries occurred?
- Which provider failed?
- What was token cost?
- Which tool was selected?

## AI-Observability Attributes

```
workflow_id
session_id
node_name
start_time
end_time
duration
tokens
provider
status
error
```