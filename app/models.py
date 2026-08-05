from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _normalize_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("title must not be blank")
    if len(stripped) > 200:
        raise ValueError("title must be at most 200 characters")
    return stripped


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _normalize_title(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _normalize_title(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime


def _normalize_comment_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be blank")
    if len(stripped) > 1000:
        raise ValueError("comment text must be at most 1000 characters")
    return stripped


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_comment_text(value)


class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    task_id: str
    text: str
    created_at: datetime


class ActivityEventType(str, Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    STATUS_CHANGED = "status_changed"
    TASK_DELETED = "task_deleted"
    COMMENT_ADDED = "comment_added"
    COMMENT_DELETED = "comment_deleted"


class ActivityEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    task_id: str
    event_type: ActivityEventType
    message: str
    details: Optional[dict[str, str]] = None
    created_at: datetime


class BulkDeleteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_ids: list[str]


class BulkDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deleted: list[str]
    not_found: list[str]
