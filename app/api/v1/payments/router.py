from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.api.v1.auth.deps import get_current_user_id
from app.api.v1.payments.schemas import PaymentCreate, PaymentRead
from app.api.v1.payments.service import PaymentService

payments_router = APIRouter(prefix="/payments", tags=["Payments"])
service = PaymentService()


@payments_router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        return await service.create_payment(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@payments_router.get("/subscription/{sub_id}", response_model=list[PaymentRead])
async def list_subscription_payments(
        sub_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user_id)
):
    return await service.get_subscription_payments(db, sub_id, user_id)
