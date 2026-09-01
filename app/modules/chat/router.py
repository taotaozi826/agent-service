from typing import Annotated

from fastapi import APIRouter, Depends, Request, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import PlainTextResponse

from .schemas import ChatRequest
from .service import ChatService
from app.infra.database import get_session

router = APIRouter(prefix="/api/v1/chat", tags=["与AI对话接口"])


def get_chat_service(
        request: Request,
        session: AsyncSession = Depends(get_session),

):
    return ChatService(session, request.app.state.agent)


# 1.阻塞式聊天返回
# @router.post("", summary="用户聊天", response_class=PlainTextResponse)
# async def chat(
#         body: ChatRequest,
#         user_id: Annotated[int, Header(alias="x-user-id")],
#         service: ChatService = Depends(get_chat_service)
# ):
#     # 1.调用
#     response = await service.chat_stream(user_id, body)
#     # 2.返回
#     return response

# 2.测试sse
# @router.post("", summary="用户聊天", response_class=EventSourceResponse)
# async def chat(
#         body: ChatRequest,
#         user_id: Annotated[int, Header(alias="x-user-id")],
#         service: ChatService = Depends(get_chat_service)
# ):
#    for i in range(100):
#        yield ServerSentEvent(data=f"message_{i}", event="message")
#    yield ServerSentEvent(data="[DONE]", event="done")

# 3. 流式输出回答
@router.post("", summary="用户聊天", response_class=EventSourceResponse)
async def chat(
        body: ChatRequest,
        user_id: Annotated[int, Header(alias="x-user-id")],
        service: ChatService = Depends(get_chat_service)
):
    # Generator, 用yield不断生成内容，形成动态列表
    async for text in service.chat_stream(user_id=user_id, request=body):
        yield text

