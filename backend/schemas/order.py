from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class OrderBase(BaseModel):
    order_number: str
    customer_name: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = 0
    priority: Optional[str] = "NORMAL"
    status: Optional[str] = "PENDING"
    deadline: Optional[datetime] = None
    progress: Optional[float] = 0.0

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    progress: Optional[float] = None

class OrderResponse(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
