.PHONY: help install dev test lint format clean docker-up docker-down

help:
	@echo "TravelPilot AI Management Commands"
	@echo "------------------------------------"
	@echo "install     : Install backend dependencies"
	@echo "dev         : Start FastAPI backend dev server"
	@echo "test        : Run backend automated test suite"
	@echo "lint        : Run code linting"
	@echo "format      : Run code formatters"
	@echo "clean       : Remove temporary cache files"
	@echo "docker-up   : Run services via Docker Compose"
	@echo "docker-down : Stop Docker Compose services"

install:
	pip install -e .[dev]

dev:
	uvicorn backend.app.main:app --reload --port 8000

test:
	pytest backend/tests/ -v

lint:
	ruff check backend/ app/

format:
	ruff format backend/ app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
