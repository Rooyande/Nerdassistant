from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.db import Base


class Duel(Base):
    __tablename__ = "duels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)   # گروهی که duel در آن ساخته شده
    created_by: Mapped[int] = mapped_column(BigInteger, index=True)  # user_id سازنده

    # فعلاً فقط steps. بعداً می‌تونه sleep/workout هم باشه
    metric: Mapped[str] = mapped_column(String(32), default="steps", nullable=False)

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False)
    # pending → active → finished → cancelled

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
