from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductItemResponse(BaseModel):
    """单个保险产品返回实体，完全对齐前端样例JSON"""
    id: int = Field(description="产品主键")
    name: str = Field(max_length=200, description="商城展示名称")
    clause_name: str = Field(max_length=300, description="主条款文件名，包含 .pdf 后缀")
    category: str = Field(max_length=50, description="险种分类")
    insurer: str = Field(max_length=120, description="承保保险公司")
    image_url: Optional[str] = Field(None, description="产品展示图片地址")
    description: Optional[str] = Field(None, description="产品简介")
    # 注意：前端接收字符串格式金额 "255.00"，数据库是 Numeric(14,2)，pydantic支持 Decimal <-> str 自动序列化
    min_premium: Decimal | None
    max_premium: Decimal | None
    target_group: Optional[str] = Field(None, max_length=300, description="适用人群说明")
    highlights: Optional[List[str]] = Field(None, description="产品亮点列表")
    status: str = Field(max_length=30, description="产品状态")


