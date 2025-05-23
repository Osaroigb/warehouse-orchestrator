from app.models.base import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class RobotTask(Base):
    __tablename__ = "robot_tasks"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))