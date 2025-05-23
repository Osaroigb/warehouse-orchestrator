from faker import Faker

fake = Faker()

def generate_order_payload(order_ref: str = None):
    return {
        "platform": "ubereats",
        "order_ref": order_ref or f"UE-{fake.uuid4()[:8]}",
        "delivery_eta": fake.future_datetime(end_date="+30d").isoformat(),
        "items": [
            {"sku": fake.lexify(text="SKU-?????"), "quantity": fake.random_int(min=1, max=5)},
            {"sku": fake.lexify(text="SKU-?????"), "quantity": fake.random_int(min=1, max=5)},
        ]
    }

def assert_error_response(response, expected_status: int, expected_error_type: str):
    assert response.status_code == expected_status
    body = response.json()

    assert body["success"] is False
    assert body["data"]["error_type"] == expected_error_type