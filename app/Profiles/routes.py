

from fastapi import APIRouter, Depends

from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import app.Profiles.crudPatientsProfile as crudPatient
import app.Profiles.crudDoctorsProfile as crudDoctors
from app.schemas import PatienceProfileJson as p_Json
from app.schemas import DoctorsProfileJson as d_Json
routerProfiles = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@routerProfiles.get("/profile/Patients/get{id}")
async def getByID(id:int,db:db_dependency):
    return crudPatient.getById(id,db)
@routerProfiles.post("/profile/Patients/create")
async def create(patient:p_Json,db:db_dependency):
    crudPatient.create(patient,db)

@routerProfiles.post("/profile/Patients/update/{id}")
async def update(patient:p_Json,db:db_dependency,id:int):
  return  crudPatient.update(patient,db,id)
@routerProfiles.delete("/profile/Patients/delete/{id}")
async def delete(id:int,db:db_dependency):
    crudPatient.delete(id,db)


@routerProfiles.get("/profile/Doctors/get{id}")
async def getByID(id: int, db: db_dependency):
    return crudDoctors.getById(id, db)


@routerProfiles.post("/profile/Doctors/create")
async def create(patient: p_Json, db: db_dependency):
    crudDoctors.create(patient, db)


@routerProfiles.post("/profile/Doctors/update/{id}")
async def update(patient: p_Json, db: db_dependency, id: int):
    return crudDoctors.update(patient, db, id)


@routerProfiles.delete("/profile/Doctors/delete/{id}")
async def delete(id: int, db: db_dependency):
    crudDoctors.delete(id, db)