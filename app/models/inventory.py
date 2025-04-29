from app.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    stock = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)