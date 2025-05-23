from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import APIRouter, Depends, status
from app.schemas.order_schema import OrderCreate
from app.utils.api_responses import build_success_response
from app.services.order_service import create_order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = create_order_service(payload, db)

    return build_success_response(
        message="Order received successfully",
        status=status.HTTP_201_CREATED,
        data={"order_id": order.id}
    )