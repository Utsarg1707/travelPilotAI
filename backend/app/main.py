"""
TravelPilot AI - Backend Main FastAPI Entrypoint
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api import travel_router
from backend.app.config.settings import settings
from backend.app.models import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for database initialization."""
    init_db()
    yield


app = FastAPI(
    title="TravelPilot AI",
    description="Production-oriented Agentic AI Travel Planning & Decision-Support System",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(travel_router)


@app.get("/api/v1/health", tags=["System Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": "TravelPilot AI", "mode": settings.APP_MODE}


@app.get("/api/v1/ready", tags=["System Health"])
async def readiness_check():
    """Readiness probe endpoint."""
    return {"status": "ready"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler returning clean structured error responses."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "detail": str(exc),
        },
    )
