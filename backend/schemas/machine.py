from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class MachineBase(BaseModel):
    name: str
    machine_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = "OPERATIONAL"
    health_status: Optional[str] = "GOOD"

class MachineCreate(MachineBase):
    pass

class MachineUpdate(BaseModel):
    name: Optional[str] = None
    machine_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    health_status: Optional[str] = None

class MachineResponse(MachineBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
