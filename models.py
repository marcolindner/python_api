from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    total_price: Optional[float] = None
    tax: float
    amount: int