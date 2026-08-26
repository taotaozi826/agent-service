from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

"""创建会话请求体"""
class ChatThreadCreateRequest(BaseModel):
    title: str = Field(default="新会话", min_length=1, max_length=200)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        return value.strip()


"""会话响应实体"""
class ChatThreadResponse(BaseModel):
    id: UUID = Field(description="会话ID，也是LangGraph thread_id")
    title: str = Field(description="会话标题")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")

    model_config = {"from_attributes": True}