from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import InsurancePlanRepository
from .schemas import InsurancePlanCreate


class InsurancePlanService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = InsurancePlanRepository(session)

    async def create_plan(self, user_id: int, data: InsurancePlanCreate)->UUID:
        """
        创建保险方案
        :param user_id: 用户ID
        :param data: 保险方案数据
        :return: 保险方案ID
        """
        async with self.session.begin():
           res =  await self.repository.create(user_id, data)
           return res.id