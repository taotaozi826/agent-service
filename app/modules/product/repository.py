from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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
