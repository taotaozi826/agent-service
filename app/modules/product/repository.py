from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_products(self, category: str | None) -> Sequence[Product]:
        # 方法1: 写死查询条件, 不推荐
        # products = await self.session.execute(
        #     select(Product)
        #     .where(Product.category == category and Product.status == 'active')
        #     .order_by(Product.id.asc())
        # )
        # return products.scalars().all()

        # 方案2
        conditions = [Product.status == 'active']
        if category:
            conditions.append(Product.category == category)

        products = await self.session.execute(
            select(Product)
            .where(*conditions))
        return products.scalars().all()

        products = await self.session.scalars(
            select(Product)
            .where(*conditions))
        return products.all()


