# Makefile for Advanced Intelligent Q&A Chatbot

PYTHON ?= python3
PIP ?= pip3
VENV ?= .venv
ACTIVATE = . $(VENV)/bin/activate

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make setup          - Create venv and install requirements"
	@echo "  make run-backend    - Run FastAPI backend (localhost:8000)"
	@echo "  make run-frontend   - Run Streamlit frontend (localhost:8501)"
	@echo "  make run            - Run both frontend and backend"
	@echo "  make test           - Run tests"
	@echo "  make docker-build   - Build docker images"
	@echo "  make docker-up      - Start with docker-compose"
	@echo "  make docker-down    - Stop docker-compose"

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -U pip

.PHONY: setup
setup: $(VENV)/bin/activate
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: run-backend
run-backend:
	$(ACTIVATE) && uvicorn backend.app.main:app --host 0.0.0.0 --port $${BACKEND_PORT:-8000} --reload

.PHONY: run-frontend
run-frontend:
	$(ACTIVATE) && streamlit run frontend/app.py --server.address 0.0.0.0 --server.port $${FRONTEND_PORT:-8501}

.PHONY: run
run:
	$(ACTIVATE) && \
	(uvicorn backend.app.main:app --host 0.0.0.0 --port $${BACKEND_PORT:-8000} --reload & \
	streamlit run frontend/app.py --server.address 0.0.0.0 --server.port $${FRONTEND_PORT:-8501} & \
	wait)

.PHONY: test
test:
	$(ACTIVATE) && pytest -q

.PHONY: docker-build
docker-build:
	docker compose build --no-cache

.PHONY: docker-up
docker-up:
	docker compose up -d

.PHONY: docker-down
docker-down:
	docker compose down
