
import json

from src.handler import lambda_handler


def make_event(method="POST", path="/fulfill", body=None):
    return {
        "requestContext": {
            "http": {
                "method": method
            }
        },
        "rawPath": path,
        "body": json.dumps(body) if body is not None else None
    }


def test_fulfill_success():
    event = make_event(
        body={
            "order_id": "ORD-001",
            "supplier_id": "SupplierA",
            "product_id": "GAME-001",
            "account_id": "Acc001"
        }
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200


def test_unknown_endpoint():
    event = make_event(
        method="POST",
        path="/unknown"
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 404

    body = json.loads(result["body"])

    assert body["error"] == "Not found"


def test_unsupported_method():
    event = make_event(
        method="GET",
        path="/fulfill"
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 404


def test_missing_order_id():
    event = make_event(
        body={
            "supplier_id": "SupplierA",
            "product_id": "GAME-001"
        }
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 400


def test_missing_supplier_id():
    event = make_event(
        body={
            "order_id": "ORD-001",
            "product_id": "GAME-001"
        }
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 400


def test_missing_product_id():
    event = make_event(
        body={
            "order_id": "ORD-001",
            "supplier_id": "SupplierA"
        }
    )

    result = lambda_handler(event, None)

    assert result["statusCode"] == 400


def test_invalid_json():
    event = {
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "rawPath": "/fulfill",
        "body": "{invalid-json"
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 400

    body = json.loads(result["body"])

    assert "error" in body


def test_empty_body():
    event = make_event(body={})

    result = lambda_handler(event, None)

    assert result["statusCode"] == 400
