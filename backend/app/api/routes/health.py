"""Health route used by CI and local smoke checks."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return a simple liveness payload."""
    return {"status": "ok"}
