from __future__ import annotations
from datetime import date
from decimal import Decimal
import enum
import typing as t

from sqlalchemy import String, Numeric, Date, Enum, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if t.TYPE_CHECKING:
    from app.api.v1.payments.models import Payment
    from app.api.v1.auth.models import User


class SubscriptionPeriod(str, enum.Enum):
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

    @property
    def delta_args(self) -> dict:
        return {
            SubscriptionPeriod.weekly: {'weeks': 1},
            SubscriptionPeriod.monthly: {'months': 1},
            SubscriptionPeriod.yearly: {'years': 1},
        }[self]


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    canceled = "canceled"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="subscriptions"
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="USD"
    )

    period: Mapped[SubscriptionPeriod] = mapped_column(
        Enum(
            SubscriptionPeriod,
            name="subscription_period",
            native_enum=True,
        ),
        nullable=False,
    )

    next_billing_date: Mapped[date] = mapped_column(Date, nullable=False)

    category: Mapped[str | None] = mapped_column(String)

    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(
            SubscriptionStatus,
            name="subscription_status",
            native_enum=True,
        ),
        nullable=False,
        default=SubscriptionStatus.active,
        server_default=text("'active'"),
    )

    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )
