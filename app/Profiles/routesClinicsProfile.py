


from fastapi import APIRouter, Depends
import app.OAuth2Config as Auth
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import app.Profiles.crudPatientsProfile as crudPatient
import app.Profiles.crudDoctorsProfile as crudDoctors
import app.Profiles.crudClinicsProfile as crudClinics
from app.schemas import PatienceProfileJson as p_Json
from app.schemas import DoctorsProfileJson as d_Json
from app.schemas import ClinincsProfileJson as c_Json
routerProfiles = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
@routerProfiles.post("/profile/Clinics/update/")
async def update(token:str,clinic: c_Json,db: db_dependency ):
    login = Auth.decode_access_token(token)
    crudClinics.updateClinicsProfile(clinic,db,login)

@routerProfiles.get("/profile/Clinics/get/")
async def getClinics(token:str, db: db_dependency):
    login = Auth.decode_access_token(token)
    return crudClinics.getClinicsProfileByName(login,db)