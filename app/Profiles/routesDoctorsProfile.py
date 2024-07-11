


from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.Profiles import crudPatientsProfile
from app.Profiles import crudDoctorsProfile
from starlette import status
from app.schemas import changePass, TokenData
from app.schemas import patients_json, Response
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import doctors_json ,d_check, Number
import app.OAuth2Config as Auth
import app.whatsappConfigs as whatsapp
from app.Doctors import crud as d_crud

from fastapi import APIRouter, Depends

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
async def get_current_doctor(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
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
    doctor = d_crud.checkByLogin(token_data.username,db)
    if doctor is None:
        raise credentials_exception
    return doctor

async def get_current_active_doctor(
    current_doctor: Annotated[d_check, Depends(get_current_doctor)]
):

    return current_doctor





@routerProfiles.get("/profile/Doctors")
async def getByID(current_user: Annotated[d_check, Depends(get_current_active_doctor)], db: db_dependency):
    return crudDoctors.getByPhone(current_user.phone, db)


@routerProfiles.post("/profile/Doctors/create")
async def create(patient: d_Json, db: db_dependency):
    crudDoctors.create(patient, db)


@routerProfiles.post("/profile/Doctors/update")
async def update(current_user: Annotated[d_check, Depends(get_current_active_doctor)],patient: d_Json, db: db_dependency, id: int):
    return crudDoctors.update(patient, db, current_user.phone)


@routerProfiles.delete("/profile/Doctors/delete")
async def delete(current_user: Annotated[d_check, Depends(get_current_active_doctor)], int, db: db_dependency):
    crudDoctors.delete(current_user.phone, db)