from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat_thread.models import ChatThread


class ChatThreadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 1.新建会话
    async def add(self, chat_thread: ChatThread):
        self.session.add(chat_thread)

    # 2.根据用户id查询所有会话
    async def list_by_user(self, user_id: int) -> list[ChatThread]:
        result = await self.session.execute(
            select(ChatThread)
            .where(ChatThread.user_id == user_id)
            .order_by(ChatThread.updated_at.desc(), ChatThread.created_at.desc())
        )
        return list(result.scalars().all())

    # 3.修改会话名(实际是找到对应的orm对象给业务层, 让业务层修改)
    async def find_owned(self, user_id: int, thread_id: UUID) -> ChatThread | None:
        result = await self.session.execute(
            select(ChatThread)
            .where(ChatThread.user_id == user_id, ChatThread.id == thread_id)
        )
        return result.scalar_one_or_none()

    # 4.删除会话
    async def delete_thread(self, thread: ChatThread) -> None:
        await self.session.delete(thread)
