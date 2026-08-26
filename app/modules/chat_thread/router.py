from uuid import UUID
from fastapi import APIRouter, Header, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ChatThreadCreateRequest, ChatThreadResponse
from .service import ChatThreadService
from ...infra.database import get_session

router = APIRouter(prefix='/api/v1/chat-threads', tags=['会话管理'])


# 1.新建会话
@router.post('', summary='创建会话', response_model=ChatThreadCreateRequest)
async def create_chat_thread(
        body: ChatThreadCreateRequest,
        user_id: int = Header(alias="x-user-id"),
        session: AsyncSession = Depends(get_session),
):
    service = ChatThreadService(session)
    return await service.add(user_id, body.title)


# 2.根据用户id查询所有会话
@router.get('', summary='查询会话列表', response_model=list[ChatThreadResponse])
async def list_chat_threads(
        user_id: int = Header(alias="x-user-id"),
        session: AsyncSession = Depends(get_session),
):
    service = ChatThreadService(session)
    return await service.list_by_user(user_id)


# 3.重命名会话名称
@router.patch('/{thread_id}', summary='重命名会话名称', response_model=ChatThreadResponse)
async def rename_thread(
        body: ChatThreadCreateRequest,
        thread_id: UUID,
        user_id: int = Header(alias="x-user-id"),
        session: AsyncSession = Depends(get_session),
):
    service = ChatThreadService(session)
    return await service.rename(user_id, thread_id, body.title)


# 4.删除指定会话
@router.delete('/{thread_id}', summary='删除指定会话', status_code=status.HTTP_204_NO_CONTENT)
async def del_thread(
        thread_id: UUID,
        user_id: int = Header(alias="x-user-id"),
        session: AsyncSession = Depends(get_session),
):
    service = ChatThreadService(session)
    await service.delete_thread(user_id, thread_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
