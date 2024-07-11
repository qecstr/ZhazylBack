
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, Depends

from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import app.Profiles.crudPatientsProfile as crudPatient
import app.Profiles.crudDoctorsProfile as crudDoctors
import app.Profiles.crudClinicsProfile as crudClinics
from app.schemas import PatienceProfileJson as p_Json, TokenData, p_check
from app.schemas import DoctorsProfileJson as d_Json
from app.schemas import ClinincsProfileJson as c_Json
from starlette import status
from app.Patients import crud as p_crud
routerProfiles = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


async def get_current_patient(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")

        if phone is None:
            raise credentials_exception
        token_data = TokenData(username=phone)
    except JWTError:
        raise credentials_exception
    patient = p_crud.checkByLogin(token_data.username,db)
    if patient is None:
        raise credentials_exception
    return patient

async def get_current_active_patient(
    current_patient: Annotated[p_check, Depends(get_current_patient)]
):

    return current_patient
@routerProfiles.get("/profile/Patients/get")
async def getByID(
        current_user: Annotated[p_check, Depends(get_current_active_patient)],
                  db:db_dependency
):
    id = crudPatient.getPatientbyPhone(current_user.phone,db).id
    return crudPatient.getById(id,db)
@routerProfiles.post("/profile/Patients/create")
async def create(patient:p_Json,db:db_dependency):
    crudPatient.create(patient,db)

@routerProfiles.post("/profile/Patients/update")
async def update(patient:p_Json,db:db_dependency,
                 current_user: Annotated[p_check, Depends(get_current_active_patient)],):
  id = crudPatient.getPatientbyPhone(current_user.phone, db).id
  return crudPatient.update(patient,db,id)
@routerProfiles.delete("/profile/Patients/delete")
async def delete(current_user: Annotated[p_check, Depends(get_current_active_patient)],db:db_dependency):
    id = crudPatient.getPatientbyPhone(current_user.phone, db).id
    crudPatient.delete(id,db)

