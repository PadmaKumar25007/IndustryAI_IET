from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.db.database import get_db

from backend.models.models import ProductionRun
from backend.schemas.production import ProductionRunCreate, ProductionRunUpdate, ProductionRunResponse

router = APIRouter()

@router.post("", response_model=ProductionRunResponse)
def create_production(production: ProductionRunCreate, db: Session = Depends(get_db)):
    db_prod = ProductionRun(**production.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@router.get("", response_model=List[ProductionRunResponse])
def get_productions(
    status: Optional[str] = None, 
    order_id: Optional[UUID] = None,
    machine_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProductionRun)
    if status: query = query.filter(ProductionRun.status == status)
    if order_id: query = query.filter(ProductionRun.order_id == order_id)
    if machine_id: query = query.filter(ProductionRun.machine_id == machine_id)
    return query.all()

@router.get("/{production_id}", response_model=ProductionRunResponse)
def get_production(production_id: UUID, db: Session = Depends(get_db)):
    db_prod = db.query(ProductionRun).filter(ProductionRun.id == production_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Production run not found")
    return db_prod

@router.put("/{production_id}", response_model=ProductionRunResponse)
def update_production(production_id: UUID, production: ProductionRunUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(ProductionRun).filter(ProductionRun.id == production_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Production run not found")
    update_data = production.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_prod, key, value)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@router.delete("/{production_id}")
def delete_production(production_id: UUID, db: Session = Depends(get_db)):
    db_prod = db.query(ProductionRun).filter(ProductionRun.id == production_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Production run not found")
    db.delete(db_prod)
    db.commit()
    return {"message": "Production run deleted"}
