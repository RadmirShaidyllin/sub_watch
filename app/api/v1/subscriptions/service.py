from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from app.api.v1.subscriptions.models import Subscription
from app.api.v1.subscriptions.schemas import SubscriptionCreate, SubscriptionUpdate
from app.api.v1.subscriptions.utils import calculate_next_billing_date


class SubscriptionService:
    async def create(self, db: AsyncSession, user_id: int, schema: SubscriptionCreate) -> Subscription:
        data = schema.model_dump()
        today = date.today()

        if not data.get("next_billing_date") or data.get("next_billing_date") == today:
            data["next_billing_date"] = calculate_next_billing_date(
                today,
                schema.period
            )

        subscription = Subscription(user_id=user_id, **data)
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        return subscription

    async def get_user_subs(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalars().all()
