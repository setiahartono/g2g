import random, uuid
from abc import ABC, abstractmethod


class SupplierBase(ABC):
    success_rate = 100

    @abstractmethod
    def transform_request(self, order: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def transform_response(self, response: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def return_mock_response(self, transaction_id: str, status_code: int) -> dict:
        # Simulate Supplier's original response
        raise NotImplementedError

    def mock_api_call(self, order: dict) -> dict:
        status_code = 200
        transaction_id = str(uuid.uuid4())
        if random.uniform(0, 100) > self.success_rate:
            # Simulating unreliability dependent on success rate
            status_code = 502
            transaction_id = None

        return self.return_mock_response(transaction_id, status_code)

    def fulfill(self, order: dict) -> dict:
        payload = self.transform_request(order)
        response = self.mock_api_call(payload)
        return self.transform_response(response)
