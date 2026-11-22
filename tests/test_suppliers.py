
from suppliers.supplier_a import SupplierA
from suppliers.supplier_b import SupplierB


ORDER = {
    "order_id": "ORD-001",
    "supplier_id": "SupplierA",
    "product_id": "GAME-001",
    "account_id": "PLAYER-123",
}


class TestSupplierA:
    def setup_method(self):
        self.adapter = SupplierA()

    def test_transform_request(self):
        result = self.adapter.transform_request(ORDER)

        assert result == {
            "user_id": "PLAYER-123",
            "product_code": "GAME-001",
            "reference": "ORD-001",
        }

    def test_transform_success_response(self):
        response = {
            "status": "SUCCESS",
            "transaction_id": "SUP-A-123",
            "message": "Top-up successful",
        }

        result = self.adapter.transform_response(response)

        assert result == {
            "status": "SUCCESS",
            "supplier_reference": "SUP-A-123",
            "error": None,
            "retryable": False,
        }

    def test_transform_failure_response(self):
        response = {
            "status": "ERROR",
            "error_code": "SERVICE_UNAVAILABLE",
            "message": "Supplier service is unavailable",
        }

        result = self.adapter.transform_response(response)

        assert result["status"] == "FAILED"
        assert result["supplier_reference"] is None
        assert result["retryable"] is True

    def test_fulfill_pipeline(self, monkeypatch):
        raw_response = {
            "status": "SUCCESS",
            "transaction_id": "SUP-A-123",
            "message": "Top-up successful",
        }

        monkeypatch.setattr(
            self.adapter,
            "mock_api_call",
            lambda payload: raw_response,
        )

        result = self.adapter.fulfill(ORDER)

        assert result["status"] == "SUCCESS"
        assert result["supplier_reference"] == "SUP-A-123"


class TestSupplierB:
    def setup_method(self):
        self.adapter = SupplierB()

    def test_transform_request(self):
        result = self.adapter.transform_request(ORDER)

        assert result == {
            "customer": {
                "id": "PLAYER-123",
            },
            "sku": "GAME-001",
            "merchant_reference": "ORD-001",
        }

    def test_transform_success_response(self):
        response = {
            "code": 200,
            "data": {
                "receipt_no": "SUP-B-456",
                "message": "Transaction completed",
            },
        }

        result = self.adapter.transform_response(response)

        assert result == {
            "status": "SUCCESS",
            "supplier_reference": "SUP-B-456",
            "error": None,
            "retryable": False,
        }

    def test_transform_failure_response(self):
        response = {
            "code": 503,
            "error": {
                "message": "Temporarily unavailable",
            },
        }

        result = self.adapter.transform_response(response)

        assert result["status"] == "FAILED"
        assert result["supplier_reference"] is None
        assert result["retryable"] is True

    def test_fulfill_pipeline(self, monkeypatch):
        raw_response = {
            "code": 200,
            "data": {
                "receipt_no": "SUP-B-456",
                "message": "Transaction completed",
            },
        }

        monkeypatch.setattr(
            self.adapter,
            "mock_api_call",
            lambda payload: raw_response,
        )

        result = self.adapter.fulfill(ORDER)

        assert result["status"] == "SUCCESS"
        assert result["supplier_reference"] == "SUP-B-456"
