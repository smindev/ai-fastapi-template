# ai-fastapi-template

A clean FastAPI template for building AI-powered backends with OpenAI. It includes a modular structure, environment-based configuration, structured logging, global error handling, Docker support, and a sample `/generate` endpoint.

## Features
- FastAPI (Python 3.11+)
- Modular routers: `routes/`, `services/`, `schemas/`
- OpenAI integration via a simple `AIService`
- Env vars loaded from `.env` with `python-dotenv`
- Structured logging and global error handlers
- Example endpoint: `POST /generate`
- Dockerfile, requirements, pytest test

## Quickstart

1) Create and fill your `.env` file:

```
OPENAI_API_KEY=sk-...
# Optional
OPENAI_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
```

2) Install dependencies and run locally:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000/docs to try the API.

3) Example request

```
POST /generate
{
  "prompt": "Write a haiku about FastAPI"
}
```

Response:
```
{
  "text": "...",
  "model": "gpt-4o-mini"
}
```

## Project layout

- `main.py` — app factory, logging, CORS, error handlers, routes
- `routes/` — FastAPI routers (e.g., `generate.py`)
- `services/` — business logic and integrations (e.g., `ai_service.py`)
- `schemas/` — Pydantic models for request/response
- `tests/` — pytest tests

## Testing

```
pip install -r requirements.txt
pytest -q
```

## Docker

Build and run:

```
docker build -t ai-fastapi-template .
docker run -it --rm -p 8000:8000 \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --env OPENAI_MODEL=gpt-4o-mini \
  ai-fastapi-template
```

## Notes
- The `/generate` endpoint is intentionally simple; extend `AIService` for more advanced use-cases (system prompts, tools, streaming, etc.).
- All secrets should be provided via env vars or a mounted `.env` file in production.
