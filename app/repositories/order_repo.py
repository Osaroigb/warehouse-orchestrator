from typing import Optional
from sqlalchemy.orm import Session
from app.models.order import Order
from app.core.config import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.warehouse import Warehouse
from app.models.order_item import OrderItem
from app.utils.errors import DatabaseCommitError
from app.constants.enums import WarehouseStatus, RobotStatus, InventoryStatus

def get_order_by_ref(db: Session, order_ref: str) -> Optional[Order]:
    return db.query(Order).filter(Order.order_ref == order_ref).first()


def get_available_warehouse(db: Session) -> Warehouse | None:
    return db.query(Warehouse).filter(
        Warehouse.status == WarehouseStatus.ACTIVE,
        Warehouse.robot_status == RobotStatus.ONLINE,
        Warehouse.inventory_status == InventoryStatus.SYNCED
    ).first()


def create_order(db: Session, order: Order) -> Order:
    db.add(order)
    db.flush()  # gets order.id populated
    return order


def add_order_items(db: Session, items: list[OrderItem]) -> None:
    db.add_all(items)


def commit_order(db: Session, order: Order) -> Order:
    try:
        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"❌ Failed to commit order to DB: {str(e)}")
        raise DatabaseCommitError("Failed to create order due to DB error. Please retry later.")