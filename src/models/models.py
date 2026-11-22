from pydantic import BaseModel, Field


class FulfillmentRequest(BaseModel):
    order_id: str = Field(min_length=1)
    supplier_id: str = Field(min_length=1)
    product_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
