import pytest
from app.main import app
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.warehouse import Warehouse
from httpx import AsyncClient, ASGITransport
from tests.utils.test_helpers import generate_order_payload, assert_error_response

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
    payload = generate_order_payload()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["order_id"]


@pytest.mark.asyncio
async def test_create_order_duplicate(sample_warehouse, db: Session):
    order_ref = "UE-DUPLICATE"
    order = Order(
        platform="ubereats",
        order_ref=order_ref,
        status="received",
        warehouse_id=sample_warehouse.id
    )
    db.add(order)
    db.commit()

    payload = generate_order_payload(order_ref=order_ref)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/", json=payload)

    assert_error_response(response, expected_status=400, expected_error_type="DUPLICATE_RESOURCE")


@pytest.mark.asyncio
async def test_create_order_missing_items(sample_warehouse):
    payload = generate_order_payload()
    payload["items"] = []

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_order_no_warehouse(db: Session):
    db.query(Warehouse).delete()
    db.commit()

    payload = generate_order_payload(order_ref="UE-NO-WH")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/orders/", json=payload)

    assert_error_response(response, expected_status=503, expected_error_type="SERVICE_UNAVAILABLE")