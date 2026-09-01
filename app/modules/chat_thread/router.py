from uuid import UUID

from fastapi import APIRouter, Depends, Header
from fastapi import Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatThread
from .schemas import ChatThreadCreateRequest, ChatThreadResponse
from .service import ThreadService
from ...infra.database import get_session

router = APIRouter(prefix="/api/v1/chat-threads", tags=['会话管理'])


# 1.新增会话
@router.post("", response_model=ChatThreadResponse)
async def create_chat_thread(
        body: ChatThreadCreateRequest,
        session: AsyncSession = Depends(get_session),
        user_id: int = Header(alias='x-user-id')
) -> ChatThreadResponse:
    service = ThreadService(session)
    return await service.add_thread(body.title, user_id)


# 2.查询所有会话列表
@router.get("", response_model=list[ChatThreadResponse])
async def list_chat_threads(
        session: AsyncSession = Depends(get_session),
        user_id: int = Header(alias='x-user-id')
) -> list[ChatThread]:
    service = ThreadService(session)
    return await service.thread_list(user_id)


# 3.重命名
@router.patch("/{thread_id}", response_model=ChatThreadResponse)
async def rename_chat_thread(
        thread_id: UUID,
        body: ChatThreadCreateRequest,
        session: AsyncSession = Depends(get_session),
        user_id: int = Header(alias='x-user-id')
) -> ChatThread:
    service = ThreadService(session)
    return await service.thread_rename(user_id, thread_id, body.title)


# 4. 删除会话
@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def rename_chat_thread(
        thread_id: UUID,
        session: AsyncSession = Depends(get_session),
        user_id: int = Header(alias='x-user-id')
):
    service = ThreadService(session)
    await service.thread_delete(user_id, thread_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
