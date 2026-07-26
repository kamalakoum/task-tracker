# Defines the GET /version endpoint used to retrieve the API version.
from fastapi import APIRouter

from app import __version__
from app.schemas.version import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse, status_code=200)
def get_version() -> VersionResponse:
    """Return the API version."""
    return VersionResponse(version=__version__)
