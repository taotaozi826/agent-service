from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: UUID
    message: str = Field(min_length=1,description="用户聊天消息")

