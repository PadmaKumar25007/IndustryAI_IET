from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.db.database import get_db

from backend.models.models import Machine, MachineTelemetry
from backend.schemas.machine import MachineCreate, MachineUpdate, MachineResponse
from backend.schemas.telemetry import TelemetryResponse

router = APIRouter()

@router.post("", response_model=MachineResponse)
def create_machine(machine: MachineCreate, db: Session = Depends(get_db)):
    db_machine = Machine(**machine.model_dump())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

@router.get("", response_model=List[MachineResponse])
def get_machines(status: Optional[str] = None, health_status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Machine)
    if status:
        query = query.filter(Machine.status == status)
    if health_status:
        query = query.filter(Machine.health_status == health_status)
    return query.all()

@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: UUID, db: Session = Depends(get_db)):
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return db_machine

@router.get("/{machine_id}/telemetry", response_model=List[TelemetryResponse])
def get_machine_telemetry(machine_id: UUID, limit: int = 50, db: Session = Depends(get_db)):
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    telemetry = db.query(MachineTelemetry).filter(MachineTelemetry.machine_id == machine_id).order_by(MachineTelemetry.timestamp.desc()).limit(limit).all()
    return telemetry

@router.put("/{machine_id}", response_model=MachineResponse)
def update_machine(machine_id: UUID, machine: MachineUpdate, db: Session = Depends(get_db)):
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    update_data = machine.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_machine, key, value)
    db.commit()
    db.refresh(db_machine)
    return db_machine

@router.delete("/{machine_id}")
def delete_machine(machine_id: UUID, db: Session = Depends(get_db)):
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    db.delete(db_machine)
    db.commit()
    return {"message": "Machine deleted"}
