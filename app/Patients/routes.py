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
from app.schemas import doctors_json ,  p_check,d_check, Number
import app.OAuth2Config as Auth
import app.whatsappConfigs as whatsapp
from app.Doctors import crud as d_crud
from app.Patients import crud as p_crud
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

@router.post("/patients/reg")
async def regPatient(pj:patients_json, db:db_dependency):
    p_crud.register_Patient(pj, db)

    crudPatientsProfile.create_when_registered(pj,db,pj.phone)




@router.post("/patients/changePassword")
async def changePatientsPassword(
        current_user: Annotated[p_check, Depends(get_current_active_patient)],
        new_password:str,
        db: db_dependency):
    p_crud.changePassword(current_user.phone,new_password,db)



@router.get("/verify")
async def verify(code:str):
    if whatsapp.verify(code):
        return Response(code = "200", status = "Ok", message="Verified").dict(exclude_none=True)
    else:
        return Response(code="100", status="No", message="Not Verified").dict(exclude_none=True)
@router.post("/sendCode")
async def send(phonenumber:Number):
   print(phonenumber.number)
   return whatsapp.sendMessage(number=phonenumber.number)







@router.post("/patients/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:db_dependency
) -> Token:
    json = p_check(phone = form_data.username, password = form_data.password)
    user = p_crud.authenticate_user(json,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = p_crud.create_access_token(
        data={"sub": user.phone})
    return Token(access_token=access_token, token_type="bearer")



@router.get("/patients/users/me/", response_model=p_check)
async def read_users_me(
    current_user: Annotated[p_check, Depends(get_current_active_patient)]
):
    return current_user
