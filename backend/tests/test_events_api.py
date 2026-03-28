"""API tests for the sample upcoming-events endpoint."""
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    """Health check should return 200 and an ok status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upcoming_events_endpoint_shape() -> None:
    """Upcoming events response should match the documented contract shape."""
    response = client.get("/api/v1/events/upcoming", params={"limit": 5})
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload.get("items"), list)
    assert isinstance(payload.get("count"), int)
    assert payload["count"] == len(payload["items"])

    if payload["items"]:
        item = payload["items"][0]
        required_keys = {
            "id",
            "organization_id",
            "organization_name",
            "organization_verified",
            "title",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "status",
        }
        assert required_keys.issubset(item.keys())
