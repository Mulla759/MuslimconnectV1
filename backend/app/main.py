from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import events, health, auth
from app.db.connection import init_db
from app.config.settings import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    init_db()

    
