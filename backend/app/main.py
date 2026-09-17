"""
TravelPilot AI - Backend Main Entrypoint
FastAPI application initialization stub for Phase 1 Scaffolding.
"""

from fastapi import FastAPI

app = FastAPI(
    title="TravelPilot AI",
    description="Production-oriented Agentic AI Travel Planning & Decision-Support System",
    version="0.1.0",
)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "app": "TravelPilot AI", "mode": "demo"}


@app.get("/api/v1/ready")
async def readiness_check():
    return {"status": "ready"}
