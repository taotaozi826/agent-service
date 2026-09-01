from typing import Literal

from fastapi.encoders import jsonable_encoder
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from .schemas import InsuranceAgentContext
from app.infra.database import AsyncSessionFactory
from app.modules.insurance_plan.schemas import InsurancePlanCreate
from app.modules.insurance_plan.service import InsurancePlanService
from app.modules.product.models import Product
from app.modules.product.service import ProductService

from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductItemResponse(BaseModel):
    """单个保险产品返回实体，完全对齐前端样例JSON"""
    model_config = {"from_attributes": True}

    id: int = Field(description="产品主键")
    name: str = Field(max_length=200, description="商城展示名称")
    clause_name: str = Field(max_length=300, description="主条款文件名，包含 .pdf 后缀")
    category: str = Field(max_length=50, description="险种分类：医疗、重疾、意外或寿险")
    insurer: str = Field(max_length=120, description="承保保险公司")
    image_url: Optional[str] = Field(None, description="产品展示图片地址")
    description: Optional[str] = Field(None, description="产品简介")
    min_premium: Optional[Decimal] = Field(None, description="最低保费")
    max_premium: Optional[Decimal] = Field(None, description="最高保费")
    target_group: Optional[str] = Field(None, max_length=300, description="适用人群说明")
    highlights: Optional[List[str]] = Field(None, description="产品亮点列表")
    status: str = Field(max_length=30, description="产品状态")

@tool
async def query_candidate_products(
        categories: list[Literal['critical_illness', 'medical', 'accident', 'life']],
        premium_min: Decimal | None = None,
        limit_per_category: int = 5
):
    """
    根据险种和保费条件查询可用于推荐的候选保险产品。当用户咨询具体保险产品或需要保险产品推荐时使用。
    :param categories:需要推荐的保险分类列表(最少需要一个),保险分类标识(重疾险:critical_illness  百万医疗险:medical  意外险:accident 寿险:life)
    :param premium_min: 推荐保险的最低价格, 会返回保险最低价格低于这个值的保险产品
    :param limit_per_category: 每个分类下返回的推荐保险数量
    :return:推荐保险的字典列表
    """
    async with AsyncSessionFactory() as session:
        service = ProductService(session)

        res = await service.list_candidates(
            categories=categories,
            premium_min=premium_min,
            limit_per_category=limit_per_category,
        )
        products: list[Product] = list(res)

        # 这个写法不标准, 正确做法是使用pydantic模型
        # return jsonable_encoder(products)

        return [ProductItemResponse.model_validate(product) for product in products]

@tool
async def save_insurance_plan(
        data: InsurancePlanCreate,
        runtime:ToolRuntime[InsuranceAgentContext]
)-> dict[str, str]:
    """
    保存当前用户的保险推荐方案
    当用户确认这个方案可以或者满意的情况下调用此工具完成保险方案保存
    :param data:保险方案数据
    :param runtime:
    :return:
    """
    async with AsyncSessionFactory() as session:
        # 创建业务层对象
        insurance_plan_service  = InsurancePlanService(session)
        # 调用业务层完成保险方案保存
        plan_id = await insurance_plan_service.create_plan(
            user_id=runtime.context.user_id,
            data=data
        )

        return  {'plan_id': str(plan_id), 'message': '保险方案保存成功'}

