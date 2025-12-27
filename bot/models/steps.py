from datetime import datetime
from sqlalchemy import BigInteger, Date, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.db import Base


class StepEntry(Base):
    __tablename__ = "step_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Telegram user id
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)  # Group or private chat id

    day: Mapped[datetime.date] = mapped_column(Date, index=True, nullable=False)
    steps: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

