from decimal import Decimal
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 1.查询所有列表, 某个目录下所有列表
    async def get_product_list(self, category: str | None) -> Sequence[Product]:
        conditions = [Product.status == 'active']
        if category:
            conditions.append(Product.category == category)

        result = await self.session.execute(
            select(Product)
            .where(*conditions)
            .order_by(Product.id)
        )
        return result.scalars().all()

    # 2.查询列表, 多个分类查找, 只返回 min_premium < premium_min 的产品, 每个险种最多返回数量
    async def get_product_limit_list(
            self,
            category: str,
            premium_min: Decimal | None,
            limit_per_category: int
    ) -> Sequence[Product]:
        conditions = [
            Product.status == 'active',
            Product.category == category
        ]

        if premium_min:
            conditions.append(Product.min_premium < premium_min)

        result = await self.session.execute(
            select(Product)
            .where(*conditions)
            .order_by(
                Product.min_premium.desc().nullslast(),
                Product.id.asc()
            )
            .limit(limit_per_category)
        )
        return result.scalars().all()
