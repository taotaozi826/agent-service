from typing import AsyncGenerator

from fastapi.sse import ServerSentEvent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ChatRequest
from app.modules.chat_thread.repository import ChatThreadRepository
from app.modules.chat_thread.exceptions import ChatThreadNotFoundError


class ChatService:
    def __init__(self, session: AsyncSession, agent: CompiledStateGraph):
        self.repository = ChatThreadRepository(session)
        self.agent = agent

    # 一. 阻塞式全部输出
    # async def chat_stream(self, user_id: int, request: ChatRequest):
    #     # 1.校验会话是否属于当前用户
    #     thread = await self.repository.find_owned(user_id, request.thread_id)
    #     if thread is None:
    #         raise ChatThreadNotFoundError
    #
    #     # 2.调用Agent
    #     _input = {
    #         "messages": [HumanMessage(request.message)]
    #     }
    #     # config有两种写法
    #     # 写法1
    #     # _config = {
    #     #     "configurable": {"thread_id": str(request.thread_id)}
    #     # }
    #     # 写法2
    #     _config = RunnableConfig(configurable={'thread_id': str(request.thread_id)})
    #
    #     result = await self.agent.ainvoke(input=_input, config=_config)
    #
    #     # 3.取出最后一条AI消息
    #     ai_message = result['messages'][-1]
    #     return ai_message.content

    # 二. 流式输出
    async def chat_stream(self, user_id: int, request: ChatRequest) -> AsyncGenerator[ServerSentEvent, None]:
        # 1.校验会话是否属于当前用户
        thread = await self.repository.find_owned(user_id, request.thread_id)
        if thread is None:
            raise ChatThreadNotFoundError

        # 2.调用Agent
        _input = {
            "messages": [HumanMessage(request.message)]
        }
        _config = RunnableConfig(configurable={'thread_id': str(request.thread_id)})

        stream = await self.agent.astream_events(input=_input, config=_config, version='v3')

        async for message in stream.messages:
            async for text in message.text:
                yield ServerSentEvent(data=text, event="message")
            # 2.4.返回结束标识
        yield ServerSentEvent(data="[DONE]", event="done")
