from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.orders import crud
from app.database import SessionLocal
from app.schemas import OrdersJson
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/orders/clinic/{tokenClinic}")
async def read_orders(tokenClinic:str,db:db_dependency):

    return crud.getAllClinicsOrders(db,tokenClinic)
@router.get("/orders/patient/{patient_token}")
async def read_ordersPatient(patient_token:str,db:db_dependency):
    return crud.getAllPatinetsOrders(db,patient_token)
@router.get("/orders/doctors/{doctor_token}")
async def read_ordersDoctors(doctor_token:str,db:db_dependency):
    return crud.getAllDoctorsOrders(db,doctor_token)
@router.post("/orders/create")
async def create_order(json:OrdersJson,db:db_dependency):
    return crud.create_order(json,db)
@router.post("/orders/setDoctorId")
async def create_orderDoctorId(doctors_id:int,id:int,db:db_dependency):
    crud.setDoctorsId(doctors_id,db,id)
