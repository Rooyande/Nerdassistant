from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.db import Base


class SleepSession(Base):
    __tablename__ = "sleep_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Telegram user id
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Group or private chat id

    gn_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    gm_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reminded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

