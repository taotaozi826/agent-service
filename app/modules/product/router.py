from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.product.schemas import ProductItemResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["产品"])


# 1.获取完整列表
@router.get("", response_model=list[ProductItemResponse])
async def list_products(category: str | None = None, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    products = await service.list_products(category)
    return products


# 2.获取多个分类列表
# 这里拿到的candidates就是数组
@router.get("/candidates", response_model=list[ProductItemResponse])
async def list_candidates(
        categories: list[str] = Query(min_length=1),
        premium_min: Decimal | None = None,
        limit_per_category: int = 5,
        session: AsyncSession = Depends(get_session)
):
    service = ProductService(session)
    return await service.list_candidates(
        categories=categories,
        premium_min=premium_min,
        limit_per_category=limit_per_category,
    )