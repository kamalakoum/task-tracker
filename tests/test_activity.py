from app.models import TaskStatus


def test_create_task_generates_activity_event(client, created_task):
    response = client.get("/activity")

    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 1
    created = next(event for event in events if event["event_type"] == "task_created")
    assert created["task_id"] == created_task["id"]
    assert created_task["title"] in created["message"]


def test_update_task_generates_activity_event(client, created_task):
    client.patch(f"/tasks/{created_task['id']}", json={"title": "Renamed task"})

    events = client.get("/activity").json()
    updated = next(event for event in events if event["event_type"] == "task_updated")
    assert updated["task_id"] == created_task["id"]
    assert updated["details"]["title"] == "Renamed task"


def test_status_change_event_includes_from_to(client, created_task):
    client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": TaskStatus.IN_PROGRESS.value},
    )

    events = client.get("/activity").json()
    status_event = next(event for event in events if event["event_type"] == "status_changed")
    assert status_event["details"]["from"] == TaskStatus.TODO.value
    assert status_event["details"]["to"] == TaskStatus.IN_PROGRESS.value


def test_delete_task_records_activity_event(client, created_task):
    task_id = created_task["id"]
    client.delete(f"/tasks/{task_id}")

    events = client.get("/activity").json()
    deleted = next(event for event in events if event["event_type"] == "task_deleted")
    assert deleted["task_id"] == task_id
    assert created_task["title"] in deleted["message"]


def test_get_task_activity_returns_task_events(client, created_task):
    other = client.post("/tasks", json={"title": "Other task"}).json()
    client.patch(f"/tasks/{created_task['id']}", json={"description": "Changed"})

    response = client.get(f"/tasks/{created_task['id']}/activity")

    assert response.status_code == 200
    events = response.json()
    assert events
    assert all(event["task_id"] == created_task["id"] for event in events)
    assert all(event["task_id"] != other["id"] for event in events)


def test_get_task_activity_missing_task_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{missing_id}/activity")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_comment_actions_generate_activity(client, created_task):
    comment = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Note"},
    ).json()
    client.delete(f"/tasks/{created_task['id']}/comments/{comment['id']}")

    events = client.get(f"/tasks/{created_task['id']}/activity").json()
    types = {event["event_type"] for event in events}
    assert "comment_added" in types
    assert "comment_deleted" in types
