import pytest
from app.models.order import Order
from unittest.mock import MagicMock
from app.repositories import order_repo
from sqlalchemy.exc import SQLAlchemyError
from app.models.order_item import OrderItem
from app.utils.errors import DatabaseCommitError


def test_get_order_by_ref_found():
    db = MagicMock()
    expected_order = MagicMock(spec=Order)
    db.query().filter().first.return_value = expected_order
    result = order_repo.get_order_by_ref(db, "ORD-123")
    assert result == expected_order


def test_get_available_warehouse_none():
    db = MagicMock()
    db.query().filter().first.return_value = None
    result = order_repo.get_available_warehouse(db)
    assert result is None


def test_create_order_calls_flush():
    db = MagicMock()
    order = MagicMock(spec=Order)
    result = order_repo.create_order(db, order)
    db.add.assert_called_once_with(order)
    db.flush.assert_called_once()
    assert result == order


def test_add_order_items_calls_add_all():
    db = MagicMock()
    items = [MagicMock(spec=OrderItem)]
    order_repo.add_order_items(db, items)
    db.add_all.assert_called_once_with(items)


def test_commit_order_success():
    db = MagicMock()
    order = MagicMock(spec=Order)
    result = order_repo.commit_order(db, order)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(order)
    assert result == order


def test_commit_order_failure_raises():
    db = MagicMock()
    order = MagicMock(spec=Order)
    db.commit.side_effect = SQLAlchemyError("failed")

    with pytest.raises(DatabaseCommitError):
        order_repo.commit_order(db, order)