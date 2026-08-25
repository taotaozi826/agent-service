from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models import Product
from app.modules.product.repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepository(self.session)

    def list_products(self,category: str | None) -> Sequence[Product]:
        return self.repository.get_all_products(category)