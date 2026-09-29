from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.db.database import get_db

from backend.models.models import Maintenance
from backend.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse

router = APIRouter()

@router.post("", response_model=MaintenanceResponse)
def create_maintenance(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    db_maint = Maintenance(**maintenance.model_dump())
    db.add(db_maint)
    db.commit()
    db.refresh(db_maint)
    return db_maint

@router.get("", response_model=List[MaintenanceResponse])
def get_maintenances(
    status: Optional[str] = None, 
    machine_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Maintenance)
    if status: query = query.filter(Maintenance.status == status)
    if machine_id: query = query.filter(Maintenance.machine_id == machine_id)
    return query.all()

@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(maintenance_id: UUID, db: Session = Depends(get_db)):
    db_maint = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not db_maint:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return db_maint

@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(maintenance_id: UUID, maintenance: MaintenanceUpdate, db: Session = Depends(get_db)):
    db_maint = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not db_maint:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    update_data = maintenance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_maint, key, value)
    db.commit()
    db.refresh(db_maint)
    return db_maint

@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: UUID, db: Session = Depends(get_db)):
    db_maint = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not db_maint:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    db.delete(db_maint)
    db.commit()
    return {"message": "Maintenance record deleted"}
