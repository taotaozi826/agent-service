from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepository(session)

    async def list_products(self, category: str | None) -> Sequence[Product]:
        return await self.repository.get_product_list(category)
