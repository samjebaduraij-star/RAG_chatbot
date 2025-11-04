# Advanced Intelligent Q&A Chatbot with Document Processing

A sophisticated Q&A chatbot application built with Streamlit, featuring document processing capabilities, Gemini 2.5 AI integration, and comprehensive chat history management.

## 🚀 Features

### Core Functionality
- **Modern Streamlit Interface**: Clean, responsive UI with native chat components
- **Multi-format Document Support**: PDF, DOCX, TXT, and CSV file processing
- **Gemini 2.5 AI Integration**: Advanced conversational AI responses
- **Dual Chat History Storage**: Both TXT (tab-separated) and CSV formats

### Technical Features
- **Local File Storage**: No external dependencies required
- **Async Processing**: Non-blocking operations for better performance
- **Comprehensive Error Handling**: Robust exception management
- **Type Safety**: Full type hints throughout the codebase
- **Modular Architecture**: Clean separation of concerns with MVC pattern
- **Extensive Logging**: Structured logging for debugging and monitoring

## Architecture

The project follows a clean, modular structure:

- `frontend/`: Streamlit UI and client-side logic
  - `app.py`: Main Streamlit entry point
  - `src/`: UI components, core managers, services, and configs
  - `data/`: Uploaded files and chat history storage
  - `requirements.txt`: Frontend dependencies
- `backend/`: FastAPI application and API endpoints
  - `app/main.py`: FastAPI entry point (served by Uvicorn)
  - `app/api/`: REST routes for chat, documents, history
  - `app/models/`: Pydantic models
  - `app/services/`: Business Logic
  - `requirements.txt`: Backend dependencies
- `shared/`: Shared configs and schemas used by both frontend and backend
- `tests/`: Unit/integration tests
- `docker-compose.yml`: One-command multi-service orchestration
- `Makefile`: Developer convenience commands (venv, run, test, docker)
- `.env` / `.env.template`: Environment configuration

## Prerequisites

- Python 3.10+
- macOS/Linux/Windows
- (Optional) Docker 24+ and Docker Compose

## Environment Variables

Copy `.env.template` to `.env` and set your values (especially `GEMINI_API_KEY`):

```bash
cp .env.template .env
# edit .env and set GEMINI_API_KEY and any other overrides
```
Important keys:
- `GEMINI_API_KEY`: Your Google Generative AI API key
- `BACKEND_PORT`/`FRONTEND_PORT`: Optional port overrides (defaults 8000/8501)
- `UPLOAD_FOLDER`, `CHAT_HISTORY_FOLDER`: Local storage paths

## Quick Start (no Docker)

Use the included `Makefile` for a one-command setup and run:

```bash
make setup          # creates .venv and installs requirements
make run            # starts backend (8000) and frontend (8501)
```
Or run services separately:

```bash
make run-backend    # http://localhost:8000 (docs at /docs)
make run-frontend   # http://localhost:8501
```
Under the hood, these map to:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port ${FRONTEND_PORT:-8501}
```
## Run with Docker

Build and start both services using Docker Compose:

```bash
docker compose build
docker compose up -d
```
- Backend: http://localhost:8000 (Swagger UI at `/docs`)
- Frontend: http://localhost:8501

Stop the stack:

```bash
docker compose down
```
## Data & Logs

- Uploaded documents: `frontend/data/uploads/`
- Chat history: `frontend/data/chat_history/`
- Logs: `logs/`

These are mounted as volumes in Docker (see `docker-compose.yml`).

## Testing

Run tests locally:

```bash
make test
```
## Troubleshooting

- If the UI says "Please configure your GEMINI_API_KEY": ensure `.env` exists at repo root and `GEMINI_API_KEY` is set without extra spaces.
- Port already in use: set `BACKEND_PORT`/`FRONTEND_PORT` in `.env` or export env vars before running.
- PDF/DOCX processing issues: verify `frontend/data/` folders exist and are writable; ensure dependencies are installed from `requirements.txt`.
- Backend not reachable from frontend (Docker): both services are on the `chatbot-net` network in `docker-compose.yml`.

## What’s Included

- `requirements.txt`: Unified dependency spec
- `backend/requirements.txt`: Backend-only deps for lightweight images
- `backend/Dockerfile` and `frontend/Dockerfile`
- `docker-compose.yml`: One command to run the full stack
- `Makefile`: Easy local dev commands

---
Built with ❤️ using Streamlit, FastAPI, and Gemini AI.