from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class EmployeeBase(BaseModel):
    name: str
    role: str
    skills: Optional[Dict[str, Any]] = None
    certifications: Optional[Dict[str, Any]] = None
    shift: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    availability: Optional[str] = "AVAILABLE"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    skills: Optional[Dict[str, Any]] = None
    certifications: Optional[Dict[str, Any]] = None
    shift: Optional[str] = None
    status: Optional[str] = None
    availability: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
