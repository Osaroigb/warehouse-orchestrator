from sqlalchemy.orm import Session
from app.models.order import Order
from app.repositories import order_repo
from app.models.order_item import OrderItem
from app.schemas.order_schema import OrderCreate
from app.utils.errors import DuplicateResourceError, ServiceUnavailableError


def create_order_service(payload: OrderCreate, db: Session) -> Order:
    # Check for duplicate
    if order_repo.get_order_by_ref(db, payload.order_ref):
        raise DuplicateResourceError(f"Order with ref '{payload.order_ref}' already exists.")

    # Pick warehouse
    warehouse = order_repo.get_available_warehouse(db)
    if not warehouse:
        raise ServiceUnavailableError("No available warehouse to process this order.")

    # Create order
    order = Order(
        platform=payload.platform,
        order_ref=payload.order_ref,
        status="received",
        warehouse_id=warehouse.id
    )

    order_repo.create_order(db, order)

    # Add items
    items = [
        OrderItem(order_id=order.id, sku=item.sku, quantity=item.quantity, status="pending")
        for item in payload.items
    ]

    order_repo.add_order_items(db, items)

    # Commit and return
    return order_repo.commit_order(db, order)