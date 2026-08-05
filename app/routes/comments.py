from fastapi import APIRouter, HTTPException, status

from app import storage
from app.models import CommentCreate, CommentResponse

router = APIRouter(tags=["comments"])


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    """Add a comment to a task."""
    comment = storage.add_comment(task_id, payload)
    if comment is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return comment


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(task_id: str) -> list[CommentResponse]:
    """List comments for a task."""
    comments = storage.get_comments_for_task(task_id)
    if comments is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return comments


@router.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_comment(task_id: str, comment_id: str) -> None:
    """Delete a comment from a task."""
    result = storage.delete_comment(task_id, comment_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    if result is False:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id {comment_id} not found on task {task_id}",
        )
