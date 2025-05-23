import pytest
from uuid import uuid4
from app.main import app
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.warehouse import Warehouse
from httpx import AsyncClient, ASGITransport


@pytest.fixture
def sample_warehouse(db: Session):
    warehouse = Warehouse(
        location="Lagos",
        status="active",
        robot_status="online",
        inventory_status="synced"
    )

    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@pytest.mark.asyncio
async def test_create_order_success(sample_warehouse):
    payload = {
        "platform": "ubereats",
        "order_ref": f"UE-{uuid4().hex[:8]}",
        "delivery_eta": "2025-05-10T12:00:00Z",
        "items": [
            {"sku": "MILK-1L", "quantity": 1},
            {"sku": "BREAD-WHT", "quantity": 2}
        ]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["order_id"] is not None


@pytest.mark.asyncio
async def test_create_order_duplicate(sample_warehouse, db: Session):
    order = Order(
        platform="ubereats",
        order_ref="UE-DUPLICATE",
        status="received",
        warehouse_id=sample_warehouse.id
    )
    db.add(order)
    db.commit()

    payload = {
        "platform": "ubereats",
        "order_ref": "UE-DUPLICATE",
        "delivery_eta": "2025-05-10T12:00:00Z",
        "items": [{"sku": "MILK-1L", "quantity": 1}]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 400
    assert response.json()["data"]["error_type"] == "DUPLICATE_RESOURCE"


@pytest.mark.asyncio
async def test_create_order_missing_items(sample_warehouse):
    payload = {
        "platform": "ubereats",
        "order_ref": "UE-MISSING-ITEMS",
        "delivery_eta": "2025-05-10T12:00:00Z",
        "items": []
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_order_no_warehouse(db: Session):
    db.query(Warehouse).delete()
    db.commit()

    payload = {
        "platform": "ubereats",
        "order_ref": "UE-NO-WH",
        "delivery_eta": "2025-05-10T12:00:00Z",
        "items": [{"sku": "MILK-1L", "quantity": 1}]
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 503
    assert response.json()["data"]["error_type"] == "SERVICE_UNAVAILABLE"