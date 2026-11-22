
from src.suppliers import Registry


def test_fulfill_success():
    r = Registry()
    supplier_a_adapter = r.get_adapter("SupplierA")
    supplier_b_adapter = r.get_adapter("SupplierB")

    assert supplier_a_adapter.success_rate == 100
    assert supplier_b_adapter.success_rate == 80
