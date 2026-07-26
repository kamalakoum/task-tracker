# Defines the GET /version endpoint used to retrieve the API version.
from fastapi import APIRouter

from app import __version__
from app.schemas.version import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse, status_code=200)
def get_version() -> VersionResponse:
    """Retrieve the API version.

    Args:
        None

    Returns:
        VersionResponse: JSON object containing the application semantic version.

    Example:
        GET /version
        Response: {"version": "0.1.0"}
    """
    return VersionResponse(version=__version__)
