from ._base import SupplierBase


class SupplierB(SupplierBase):
    success_rate = 80

    def transform_request(self, order: dict) -> dict:
        return {
            "customer": {
                "id": order["account_id"],
            },
            "sku": order["product_id"],
            "merchant_reference": order["order_id"],
        }

    def return_mock_response(
        self,
        transaction_id: str | None,
        status_code: int
    ) -> dict:
        # Simulate Supplier B's different response format
        if status_code == 200:
            return {
                "code": 200,
                "data": {
                    "receipt_no": transaction_id,
                    "message": "Transaction completed",
                },
            }

        return {
            "code": 503,
            "error": {
                "message": "Temporarily unavailable",
            },
        }

    def transform_response(self, response: dict) -> dict:
        # Normalize Supplier B's response
        if response["code"] == 200:
            return {
                "status": "SUCCESS",
                "supplier_reference": response["data"]["receipt_no"],
                "error": None,
                "retryable": False,
            }

        return {
            "status": "FAILED",
            "supplier_reference": None,
            "error": response["error"]["message"],
            "retryable": response["code"] in (429, 500, 502, 503, 504),
        }

    def check_status(self, supplier_reference: str) -> dict:
        # Simulate Supplier B's status endpoint
        return {
            "code": 200,
            "data": {
                "receipt_no": supplier_reference,
                "transaction_status": "COMPLETED",
            },
        }