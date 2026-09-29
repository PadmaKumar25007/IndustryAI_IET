from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.db.database import get_db

from datetime import datetime
from backend.models.models import MachineTelemetry
from backend.schemas.telemetry import TelemetryCreate, TelemetryResponse

router = APIRouter()

@router.post("", response_model=TelemetryResponse)
def create_telemetry(telemetry: TelemetryCreate, db: Session = Depends(get_db)):
    # if timestamp not provided, it will use DB default (now)
    db_tel = MachineTelemetry(**telemetry.model_dump())
    db.add(db_tel)
    db.commit()
    db.refresh(db_tel)
    return db_tel

@router.get("/{machine_id}", response_model=List[TelemetryResponse])
def get_telemetry(
    machine_id: UUID,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(MachineTelemetry).filter(MachineTelemetry.machine_id == machine_id)
    if start_time:
        query = query.filter(MachineTelemetry.timestamp >= start_time)
    if end_time:
        query = query.filter(MachineTelemetry.timestamp <= end_time)
    
    # newest records first
    query = query.order_by(MachineTelemetry.timestamp.desc()).limit(limit)
    return query.all()

@router.get("/latest/{machine_id}", response_model=TelemetryResponse)
def get_latest_telemetry(machine_id: UUID, db: Session = Depends(get_db)):
    db_tel = db.query(MachineTelemetry).filter(MachineTelemetry.machine_id == machine_id).order_by(MachineTelemetry.timestamp.desc()).first()
    if not db_tel:
        raise HTTPException(status_code=404, detail="No telemetry found for this machine")
    return db_tel
