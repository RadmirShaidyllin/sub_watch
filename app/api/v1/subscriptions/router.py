from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.api.v1.auth.deps import get_current_user_id
from app.api.v1.subscriptions.schemas import SubscriptionCreate, SubscriptionRead
from app.api.v1.subscriptions.service import SubscriptionService

subscriptions_router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
service = SubscriptionService()

@subscriptions_router.post("/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return await service.create(db, user_id, data)

@subscriptions_router.get("/", response_model=list[SubscriptionRead])
async def list_subscriptions(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return await service.get_user_subs(db, user_id)