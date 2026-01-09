from __future__ import annotations
from datetime import date
from decimal import Decimal
import typing as t

from sqlalchemy import Date, Numeric, String, ForeignKey, text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if t.TYPE_CHECKING:
    from app.api.v1.subscriptions.models import Subscription


class Payment(Base):
    __tablename__ = "payments"

    __table_args__ = (
        CheckConstraint("amount > 0", name="payment_amount_positive"),
        UniqueConstraint('subscription_id', 'paid_at', name='uq_payment_period'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"),
        nullable=False,
        index=True,
    )

    subscription: Mapped["Subscription"] = relationship(
        "Subscription",
        back_populates="payments"
    )

    paid_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=text("'USD'"),
    )
