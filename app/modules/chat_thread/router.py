from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Header, Depends, Response, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ChatThreadCreateRequest, ChatThreadResponse, ChatHistoryResponse
from .service import ChatThreadService
from ...infra.database import get_session

router = APIRouter(prefix='/api/v1/chat-threads', tags=['会话管理'])


# 定义业务层的service实例, 这样每个路由不用重复定义创建
async def get_service(
        request: Request,
        session: AsyncSession = Depends(get_session),
) -> ChatThreadService:
    return ChatThreadService(
        session=session,
        agent=request.app.state.agent,
    )


# 1.新建会话
@router.post('', summary='创建会话', response_model=ChatThreadResponse)
async def create_chat_thread(
        body: ChatThreadCreateRequest,
        user_id: int = Header(alias="x-user-id"),
        service: ChatThreadService = Depends(get_service),
):
    return await service.add(user_id, body.title)


# 2.根据用户id查询所有会话
@router.get('', summary='查询会话列表', response_model=list[ChatThreadResponse])
async def list_chat_threads(
        user_id: int = Header(alias="x-user-id"),
        service: ChatThreadService = Depends(get_service),
):
    return await service.list_by_user(user_id)


# 3.重命名会话名称
@router.patch('/{thread_id}', summary='重命名会话名称', response_model=ChatThreadResponse)
async def rename_thread(
        body: ChatThreadCreateRequest,
        thread_id: UUID,
        user_id: int = Header(alias="x-user-id"),
        service: ChatThreadService = Depends(get_service),
):
    return await service.rename(user_id, thread_id, body.title)


# 4.删除指定会话
@router.delete('/{thread_id}', summary='删除指定会话', status_code=status.HTTP_204_NO_CONTENT)
async def del_thread(
        thread_id: UUID,
        user_id: int = Header(alias="x-user-id"),
        service: ChatThreadService = Depends(get_service),
):
    await service.delete_thread(user_id, thread_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 5.查询会话历史
@router.get("/{thread_id}/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
        thread_id: UUID,
        user_id: Annotated[int, Header(alias="x-user-id")],
        service: ChatThreadService = Depends(get_service),
):
    """查询指定会话的历史消息"""

    return await service.get_history(user_id, thread_id)
