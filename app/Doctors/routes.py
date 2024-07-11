
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

from app.schemas import Token
router = APIRouter()

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

@router.post("/doctors/reg")
async def regDoctor(pj:doctors_json, db:db_dependency,):
    d_crud.register_Doctor(pj, db)
    id = d_crud.checkByLogin(pj.phone,db)
    crudDoctorsProfile.createWhenAuth(pj,db,id)


@router.delete("/doctors/delete/{token}")
async def deleteDoctor(token:str,db:db_dependency):
    d_crud.delete_Doctor(token, db)

@router.post("/doctors/changePassword")
async def changePatientsPassword(current_user: Annotated[d_check, Depends(get_current_active_doctor)],new_pass:str,db: db_dependency):

    d_crud.changePassword(current_user.phone,new_pass ,db)


@router.post("/doctors/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:db_dependency
) -> Token:
    json = d_check(phone = form_data.username, password = form_data.password)
    user = d_crud.authenticate_user(json,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = d_crud.create_access_token(
        data={"sub": user.phone})
    return Token(access_token=access_token, token_type="bearer")



@router.get("patients/users/me/", response_model=d_check)
async def read_users_me(
    current_doctor: Annotated[d_check, Depends(get_current_active_doctor)]
):
    return current_doctor