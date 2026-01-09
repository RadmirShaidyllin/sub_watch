from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    subscription_id: int
    amount: Decimal = Field(gt=0)
    currency: str = "USD"
    paid_at: date = Field(default_factory=date.today)


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
