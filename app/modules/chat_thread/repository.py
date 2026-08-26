from uuid import UUID

from langchain_classic.embeddings import awa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat_thread.models import ChatThread


class ThreadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 新增会话
    async def add_thread(self, chat_thread: ChatThread):
        self.session.add(chat_thread)

    # 查询会话列表
    async def thread_list(self, user_id: int) -> list[ChatThread]:
        res = await  self.session.execute(
            select(ChatThread)
            .where(ChatThread.user_id == user_id)
            .order_by(ChatThread.created_at.desc(), ChatThread.updated_at.desc())
        )
        return list(res.scalars().all())

    # 重命名 查找到orm对象返回让业务层修改
    async def thread_find(self, user_id: int, thread_id: UUID) -> ChatThread | None:
        res = await self.session.execute(
            select(ChatThread)
            .where(ChatThread.user_id == user_id, ChatThread.id == thread_id)
        )
        return res.scalar_one_or_none()

    # 删除会话
    async def thread_delete(self, chat_thread: ChatThread):
        await self.session.delete(chat_thread)
