from .supplier_a import SupplierA
from .supplier_b import SupplierB


class Registry:
    def __init__(self):
        self.adapters = {
            "SupplierA": SupplierA(),
            "SupplierB": SupplierB(),
        }

    def get_adapter(self, supplier_id: str):
        adapter = self.adapters.get(supplier_id)

        if adapter is None:
            raise ValueError(f"Unsupported supplier: {supplier_id}")

        return adapter