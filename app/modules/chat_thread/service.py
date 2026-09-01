from uuid import UUID

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat_thread.models import ChatThread
from app.modules.chat_thread.repository import ChatThreadRepository

from app.modules.chat_thread.exceptions import ChatThreadNotFoundError
from app.modules.chat_thread.schemas import ChatHistoryResponse, ChatMessageResponse


class ChatThreadService:
    def __init__(self, session: AsyncSession,agent: CompiledStateGraph):
        self.session = session
        self.repository = ChatThreadRepository(session)
        self.agent = agent

    # 1.新建会话
    async def add(self, user_id: int, title: str):
        # 用上下文管理，开启事务，运行完成，自动commit，出现异常，自动rollback
        async with self.session.begin():
            # 创建对象，对象 映射 到数据库 一条数据
            chat_thread = ChatThread(user_id=user_id, title=title)
            # 新增对象，就是插入一条数据
            await self.repository.add(chat_thread)

        return chat_thread

    # 2.根据用户id查询所有会话
    async def list_by_user(self, user_id: int):
        return await self.repository.list_by_user(user_id)

    # 3.重命名会话名称
    async def rename(self, user_id: int, thread_id: UUID, new_title: str):
        async  with self.session.begin():
            res = await self.repository.find_owned(user_id, thread_id)
            if res is None:
                raise ChatThreadNotFoundError

            res.title = new_title

            # 更新当前的res 这个orm对象
            await self.session.flush()
            await  self.session.refresh(res)

        return res

    # 4.删除指定会话
    async def delete_thread(self, user_id: int, thread_id: UUID) -> None:
        async  with self.session.begin():
            # 1. 先找到对应的orm对象
            res = await self.repository.find_owned(user_id, thread_id)
            if res is None:
                raise ChatThreadNotFoundError

            # 2.删除checkpointer中的会话状态
            await self.agent.checkpointer.adelete_thread(str(thread_id))

            # 3.删除会话元数据
            await self.repository.delete_thread(res)

    # 5.查询会话历史
    async def get_history(self, user_id: int, thread_id: UUID)->ChatHistoryResponse:
        # 1.校验会话归属
        thread = await self.repository.find_owned(user_id, thread_id)
        if thread is None:
            raise ChatThreadNotFoundError

        # 2.读取Agent最新状态
        # config = {"configurable": {"thread_id": str(thread_id)}}
        config = RunnableConfig(configurable={'thread_id': str(thread_id)})
        snapshot = await self.agent.aget_state(config)

        # 3.只保留用户消息和AI消息
        messages = []
        for message in snapshot.values.get("messages", []):
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                continue

            if message.text:
                messages.append(
                    ChatMessageResponse(
                        role=role,
                        content=str(message.text)
                        # content=message.content # 错误写法 content = [{"type":"text","text":"实际文字"}]
                    )
                )

        return ChatHistoryResponse(
            thread_id=thread_id,
            messages=messages,
        )




