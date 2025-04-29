from app.models.base import Base
from sqlalchemy import Column, Integer, String


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)
    robot_status = Column(String, nullable=False)
    inventory_status = Column(String, nullable=False)