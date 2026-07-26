import pytest

from app import __version__


def test_get_version_returns_200_with_version(client):
    """GET /version returns 200 with the current package version."""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}
