from datetime import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.db import Base


class DuelMember(Base):
    __tablename__ = "duel_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    duel_id: Mapped[int] = mapped_column(ForeignKey("duels.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)

    role: Mapped[str] = mapped_column(String(16), default="challenger", nullable=False)
    # challenger | opponent

    status: Mapped[str] = mapped_column(String(16), default="invited", nullable=False)
    # invited | accepted | declined

    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("duel_id", "user_id", name="uq_duel_member"),
    )
