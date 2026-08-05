from fastapi import APIRouter, HTTPException

from app import storage
from app.models import ActivityEvent

router = APIRouter(tags=["activity"])


@router.get("/activity", response_model=list[ActivityEvent])
def list_activity() -> list[ActivityEvent]:
    """List all activity events, newest first."""
    return storage.get_activity()


@router.get("/tasks/{task_id}/activity", response_model=list[ActivityEvent])
def list_task_activity(task_id: str) -> list[ActivityEvent]:
    """List activity events for a single task."""
    events = storage.get_task_activity(task_id)
    if events is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return events
