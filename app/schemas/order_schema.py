from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class OrderItemCreate(BaseModel):
    sku: str = Field(..., min_length=1, example="MILK-1L")
    quantity: int = Field(..., gt=0, example=2)

    @field_validator("sku")
    def strip_sku(cls, v: str) -> str:
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "sku": "MILK-1L",
                "quantity": 2
            }
        }


class OrderCreate(BaseModel):
    platform: str = Field(..., min_length=2, example="ubereats")
    order_ref: str = Field(..., min_length=3, example="UE-123456")
    delivery_eta: datetime = Field(..., example="2025-04-11T14:00:00Z")
    items: List[OrderItemCreate] = Field(..., min_items=1)

    @field_validator("platform", "order_ref")
    def strip_fields(cls, v: str) -> str:
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "platform": "ubereats",
                "order_ref": "UE-123456",
                "delivery_eta": "2025-04-11T14:00:00Z",
                "items": [
                    {"sku": "MILK-1L", "quantity": 2},
                    {"sku": "BREAD-WHT", "quantity": 1}
                ]
            }
        }