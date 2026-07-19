# Pydantic model defining the response shape for the /health endpoint.
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Schema for the health check response."""
    status: str
    timestamp: str
