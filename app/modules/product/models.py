from decimal import Decimal

from sqlalchemy import (
    BigInteger, String, Text, Numeric, ARRAY,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base, CreateAtMixin, UpdateAtMixin


class Product(Base, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        comment="产品主键"
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="商城展示名称"
    )
    clause_name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="主条款文件名，包含 .pdf 后缀"
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="险种分类：医疗、重疾、意外或寿险"
    )
    insurer: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        comment="承保保险公司"
    )
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="产品展示图片地址"
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="产品简介"
    )
    min_premium: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    max_premium: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    target_group: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
        comment="适用人群说明"
    )
    highlights: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text()),
        nullable=True,
        comment="产品亮点列表"
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
        comment="产品状态"
    )
