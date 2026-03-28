"""Application entrypoint that wires middleware and API routes."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.config.settings import settings
from app.db.connection import ensure_initialized

app = FastAPI(title="MuslimConnect API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")


@app.on_event("startup")
def startup() -> None:
    """Ensure DB schema exists before serving traffic."""
    ensure_initialized()
