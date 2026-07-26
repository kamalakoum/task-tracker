from pydantic import BaseModel


class VersionResponse(BaseModel):
    """Schema for the version endpoint response."""
    version: str
