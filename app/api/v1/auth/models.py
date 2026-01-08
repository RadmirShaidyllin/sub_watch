from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, BigInteger, func, text, CheckConstraint
from datetime import datetime, timezone

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL) OR (tg_id IS NOT NULL)",
            name="user_email_or_tg_required",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        index=True,
    )

    tg_id: Mapped[int | None] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str | None] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),  # Генерация на стороне Python
        server_default=func.now(),
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        back_populates="user",
    )
