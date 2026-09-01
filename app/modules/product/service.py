from decimal import Decimal
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        # self.session = session
        self.repository = ProductRepository(session)

    # 1.获取完整列表
    async def list_products(self, category: str | None) -> Sequence[Product]:
        return await self.repository.get_product_list(category)

    # 2.获取多个分类列表
    async def list_candidates(
            self,
            categories: list[str],
            premium_min: Decimal | None,
            limit_per_category: int,
    ) -> list[Product]:
        candidate_products: list[Product] = []

        for category in dict.fromkeys(categories):
            products = await self.repository.find_limited_by_category(
                category=category,
                premium_min=premium_min,
                limit=limit_per_category,
            )
            candidate_products.extend(products)

        return candidate_products