from ._base import SupplierBase


class SupplierA(SupplierBase):
    def transform_request(self, order: dict) -> dict:
        return {
            "user_id": order["account_id"],
            "product_code": order["product_id"],
            "reference": order["order_id"],
        }

    def return_mock_response(
        self,
        transaction_id: str | None,
        status_code: int
    ) -> dict:
        # Simulate Supplier A's response format
        if status_code == 200:
            return {
                "status": "SUCCESS",
                "transaction_id": transaction_id,
                "message": "Top-up successful",
            }

        return {
            "status": "ERROR",
            "error_code": "SERVICE_UNAVAILABLE",
            "message": "Supplier service is unavailable",
        }

    def transform_response(self, response: dict) -> dict:
        # Normalize Supplier A's response
        if response["status"] == "SUCCESS":
            return {
                "status": "SUCCESS",
                "supplier_reference": response["transaction_id"],
                "error": None,
                "retryable": False,
            }

        return {
            "status": "FAILED",
            "supplier_reference": None,
            "error": response.get("message"),
            "retryable": response.get("error_code") == "SERVICE_UNAVAILABLE",
        }

    def check_status(self, supplier_reference: str) -> dict:
        # Simulate Supplier A's status endpoint
        return {
            "supplier_reference": supplier_reference,
            "status": "SUCCESS",
        }
