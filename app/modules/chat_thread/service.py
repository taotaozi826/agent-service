from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import ChatThreadNotFoundError
from .models import ChatThread
from .repository import ThreadRepository


class ThreadService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.thread_repository = ThreadRepository(self.session)

    # 1.创建会话
    async def add_thread(self, title: str, user_id: int):
        async with self.session.begin():
            thread = ChatThread(title=title, user_id=user_id)
            await self.thread_repository.add_thread(thread)

        return thread

    # 2.查询所有会话列表
    async def thread_list(self, user_id: int) -> list[ChatThread]:
        res = await self.thread_repository.thread_list(user_id)
        return res

    # 3.重命名
    async def thread_rename(self, user_id: int, thread_id: UUID, title: str) -> ChatThread:
        async with self.session.begin():
            res = await self.thread_repository.thread_find(user_id, thread_id)
            if res is None:
                raise ChatThreadNotFoundError
            res.title = title

            await self.session.flush()
            await self.session.refresh(res)

        return res

    # 4.删除会话
    async def thread_delete(self, user_id: int, thread_id: UUID):
        async with self.session.begin():
            res = await self.thread_repository.thread_find(user_id, thread_id)
            if res is None:
                raise ChatThreadNotFoundError
            await self.thread_repository.thread_delete(res)
