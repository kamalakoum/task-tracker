# Defines the GET /health endpoint used to verify the API is running.
from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, status_code=200)
def get_health() -> HealthResponse:
    """Check the health status of the API.

    Returns the API operational status and current UTC timestamp for synchronization.

    Args:
        None

    Returns:
        HealthResponse: JSON object with status='ok' and current UTC timestamp in ISO 8601 format.

    Example:
        GET /health
        Response: {"status": "ok", "timestamp": "2026-07-26T14:30:45.123456+00:00"}
    """
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return HealthResponse(status="ok", timestamp=current_timestamp)