from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.api.v1.payments.models import Payment
from app.api.v1.payments.schemas import PaymentCreate
from app.api.v1.subscriptions.models import Subscription
from app.api.v1.subscriptions.utils import calculate_next_billing_date


class PaymentService:
    async def create_payment(self, db: AsyncSession, user_id: int, schema: PaymentCreate) -> Payment:
        query = select(Subscription).where(
            Subscription.id == schema.subscription_id,
            Subscription.user_id == user_id
        )
        result = await db.execute(query)
        subscription = result.scalar_one_or_none()

        if not subscription:
            raise ValueError("Subscription not found or access denied")

        try:
            payment = Payment(**schema.model_dump())
            db.add(payment)

            subscription.next_billing_date = calculate_next_billing_date(
                subscription.next_billing_date,
                subscription.period
            )

            await db.commit()
            await db.refresh(payment)
            return payment
        except IntegrityError:
            await db.rollback()
            raise ValueError("Payment for this period already exists or other integrity constraint violation.")

    async def get_subscription_payments(self, db: AsyncSession, sub_id: int, user_id: int):
        query = select(Payment).join(Subscription).where(
            Payment.subscription_id == sub_id,
            Subscription.user_id == user_id
        )
        result = await db.execute(query)
        return result.scalars().all()
