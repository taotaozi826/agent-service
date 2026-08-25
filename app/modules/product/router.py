from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.product.schemas import ProductItemResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["产品"])


@router.get("", response_model=list[ProductItemResponse])
async def list_products(category: str | None = None, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    products = await service.list_products(category)
    return products
