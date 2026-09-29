from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class MaintenanceBase(BaseModel):
    machine_id: UUID
    issue: str
    description: Optional[str] = None
    technician: Optional[str] = None
    maintenance_date: Optional[datetime] = None
    resolution: Optional[str] = None
    status: Optional[str] = "PENDING"

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    issue: Optional[str] = None
    description: Optional[str] = None
    technician: Optional[str] = None
    maintenance_date: Optional[datetime] = None
    resolution: Optional[str] = None
    status: Optional[str] = None

class MaintenanceResponse(MaintenanceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
