from fastapi import APIRouter, Depends

from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from app.services import crudServices
from app.schemas import ServiceJson
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
@router.get("/service/getAll")
async def get_all_services(db:db_dependency,id:int):
    return crudServices.getAllServices(db,id)
@router.post("/service/create")
async def create_service(json:ServiceJson,db:db_dependency):
    crudServices.createService(json,db)

@router.post("/service/update/{id}")
async def update_service(json:ServiceJson,id:int,db:db_dependency):
    crudServices.updateService(json, db, id)
@router.delete("/service/delete/{id}")
async def delete_service(id:int,db:db_dependency):
    crudServices.deleteService(db, id)

@router.post("/service/setDoctorId/")
async def setDoctorId(service_id:int,doctor_id,db:db_dependency):
    crudServices.setDoctorId(db, doctor_id, service_id)
