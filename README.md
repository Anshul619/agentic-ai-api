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