def test_bulk_delete_deletes_existing_and_reports_missing(client):
    first = client.post("/tasks", json={"title": "Keep deleting 1"}).json()
    second = client.post("/tasks", json={"title": "Keep deleting 2"}).json()
    missing = "00000000-0000-0000-0000-000000000000"

    response = client.post(
        "/tasks/bulk-delete",
        json={"task_ids": [first["id"], missing, second["id"], first["id"]]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["deleted"] == [first["id"], second["id"]]
    assert body["not_found"] == [missing]
    assert client.get("/tasks").json() == []


def test_bulk_delete_empty_list_returns_empty_result(client):
    response = client.post("/tasks/bulk-delete", json={"task_ids": []})

    assert response.status_code == 200
    assert response.json() == {"deleted": [], "not_found": []}


def test_bulk_delete_unknown_field_returns_422(client):
    response = client.post("/tasks/bulk-delete", json={"task_ids": [], "extra": True})

    assert response.status_code == 422
