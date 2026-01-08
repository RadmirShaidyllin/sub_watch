from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.api.v1.subscriptions.models import SubscriptionPeriod, SubscriptionStatus


class SubscriptionBase(BaseModel):
    name: str
    amount: Decimal
    currency: str = "USD"
    period: SubscriptionPeriod
    category: str | None = None


class SubscriptionCreate(SubscriptionBase):
    next_billing_date: date | None = None


class SubscriptionUpdate(BaseModel):
    name: str | None = None
    amount: Decimal | None = None
    status: SubscriptionStatus | None = None
    next_billing_date: date | None = None


class SubscriptionRead(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: SubscriptionStatus
    next_billing_date: date