import uuid
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base, CreateAtMixin, UpdateAtMixin


class ChatThread(Base, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "chat_threads"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        comment="会话主键，同时作为 LangGraph thread_id"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="JWT 中解析出的业务用户主键"
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="新会话",
        server_default="新会话",
        comment="会话列表展示标题"
    )