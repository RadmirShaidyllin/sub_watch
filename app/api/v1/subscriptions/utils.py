from datetime import date
from dateutil.relativedelta import relativedelta

from app.api.v1.subscriptions.models import SubscriptionPeriod


def calculate_next_billing_date(current: date, period: SubscriptionPeriod) -> date:
    return current + relativedelta(**period.delta_args)
