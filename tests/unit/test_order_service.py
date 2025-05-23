import pytest
from faker import Faker
from app.models.order import Order
from unittest.mock import MagicMock, patch
from app.services.order_service import create_order_service
from app.utils.errors import DuplicateResourceError, ServiceUnavailableError

fake = Faker()

@pytest.fixture
def payload():
    return MagicMock(
        platform="ubereats",
        order_ref=fake.unique.uuid4(),
        items=[MagicMock(sku="MILK", quantity=1)],
    )


def test_create_order_success(payload):
    db = MagicMock()
    order = MagicMock(spec=Order)
    warehouse = MagicMock(id=1)

    with patch("app.repositories.order_repo.get_order_by_ref", return_value=None), \
         patch("app.repositories.order_repo.get_available_warehouse", return_value=warehouse), \
         patch("app.repositories.order_repo.create_order", return_value=order), \
         patch("app.repositories.order_repo.add_order_items"), \
         patch("app.repositories.order_repo.commit_order", return_value=order):
        result = create_order_service(payload, db)
        assert result == order


def test_duplicate_order_raises(payload):
    db = MagicMock()
    with patch("app.repositories.order_repo.get_order_by_ref", return_value=MagicMock()):
        with pytest.raises(DuplicateResourceError):
            create_order_service(payload, db)


def test_no_warehouse_raises(payload):
    db = MagicMock()
    with patch("app.repositories.order_repo.get_order_by_ref", return_value=None), \
         patch("app.repositories.order_repo.get_available_warehouse", return_value=None):
        with pytest.raises(ServiceUnavailableError):
            create_order_service(payload, db)