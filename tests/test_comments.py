def test_add_comment_returns_201(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Looks good"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Looks good"
    assert body["task_id"] == created_task["id"]
    assert body["id"]
    assert body["created_at"]


def test_add_comment_rejects_blank_text(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "   "},
    )

    assert response.status_code == 422
    assert "comment text must not be blank" in str(response.json()["detail"])


def test_add_comment_missing_task_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(f"/tasks/{missing_id}/comments", json={"text": "Hello"})

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_list_comments_for_task(client, created_task):
    client.post(f"/tasks/{created_task['id']}/comments", json={"text": "First"})
    client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Second"})

    response = client.get(f"/tasks/{created_task['id']}/comments")

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 2
    assert [comment["text"] for comment in comments] == ["First", "Second"]


def test_list_comments_missing_task_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{missing_id}/comments")

    assert response.status_code == 404


def test_delete_comment_returns_204(client, created_task):
    created = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Temporary"},
    ).json()

    response = client.delete(f"/tasks/{created_task['id']}/comments/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{created_task['id']}/comments").json() == []


def test_delete_comment_missing_comment_returns_404(client, created_task):
    missing_comment = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{created_task['id']}/comments/{missing_comment}")

    assert response.status_code == 404
    assert "Comment with id" in response.json()["detail"]


def test_delete_comment_missing_task_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{missing_id}/comments/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_comment_count_updates_on_task(client, created_task):
    client.post(f"/tasks/{created_task['id']}/comments", json={"text": "One"})
    client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Two"})

    task = client.get(f"/tasks/{created_task['id']}").json()
    assert task["comment_count"] == 2

    comments = client.get(f"/tasks/{created_task['id']}/comments").json()
    client.delete(f"/tasks/{created_task['id']}/comments/{comments[0]['id']}")

    task = client.get(f"/tasks/{created_task['id']}").json()
    assert task["comment_count"] == 1


def test_deleting_task_cascades_comments(client, created_task):
    client.post(f"/tasks/{created_task['id']}/comments", json={"text": "Will vanish"})
    client.delete(f"/tasks/{created_task['id']}")

    response = client.get(f"/tasks/{created_task['id']}/comments")
    assert response.status_code == 404
