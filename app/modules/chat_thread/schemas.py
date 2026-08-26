from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatThreadCreateRequest(BaseModel):
    """创建会话请求体"""
    title: str = Field(default="新会话", max_length=200, description="会话标题")


class ChatThreadResponse(BaseModel):
    """会话响应实体"""
    id: UUID = Field(description="会话ID，也是LangGraph thread_id")
    title: str = Field(description="会话标题")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")

    model_config = {"from_attributes": True}