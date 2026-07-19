# Defines the GET /health endpoint used to verify the API is running.
from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, status_code=200)
def get_health() -> HealthResponse:
    """Return API status and the current UTC timestamp in ISO 8601 format."""
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return HealthResponse(status="ok", timestamp=current_timestamp)