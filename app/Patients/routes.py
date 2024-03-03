from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from app.schemas import changePass
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/patients/get/{id}")
async def getById(id:int, db:db_dependency):
    return p_crud.get_Patients_by_id(id, db)
@router.post("/patients/reg")
async def regPatient(pj:patients_json, db:db_dependency):
    p_crud.register_Patient(pj, db)


@router.post("/patients/update")
async def updatePatient(id:int, db:db_dependency, pj:patients_json):
    p_crud.update_Patient(id, db, pj)
@router.delete("/patients/delete")
async def deletePatient(id:int,db:db_dependency):
    p_crud.delete_Patient(id, db)
@router.get("/patients/getAll")
async def getAllPatients(db:db_dependency):
    return p_crud.get_Patients(db)
@router.post("/patients/isExist")
async def isExists(temp :p_check, db:db_dependency):
    if p_crud.isExist(temp, db):
        return Response(status="Ok",
                    code="200",
                    message="User exists").dict(exclude_none=True)

@router.post("/patients/changePassword")
async def changePatientsPassword(temp:changePass,db: db_dependency):
    p_crud.changePassword(temp,db)

#for doctors

@router.get("/doctors/get/{id}")
async def getById(id:int, db:db_dependency):
    return d_crud.get_Doctors_by_id(id, db)
@router.post("/doctors/reg")
async def regDoctor(pj:doctors_json, db:db_dependency):
    d_crud.register_Doctor(pj, db)

@router.post("/doctors/update")
async def updateDoctor(id:int, db:db_dependency, pj:doctors_json):
    d_crud.update_Doctor(id, db, pj)
@router.delete("/doctors/delete")
async def deleteDoctor(id:int,db:db_dependency):
    d_crud.delete_Doctor(id, db)
@router.get("/doctors/getAll")
async def getAllDoctors(db:db_dependency):
    return d_crud.get_Doctors(db)
@router.post("/doctors/isExist")
async def isExists(temp :d_check, db:db_dependency):
    if p_crud.isExist(temp, db):
        return Response(status="Ok",
                        code="200",
                        message="User exists").dict(exclude_none=True)


@router.post("/doctors/changePassword/{login}/{newPassword}")
async def changePatientsPassword(temp:changePass,db: db_dependency):
    d_crud.changePassword(temp,db)



#не рабочее



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



@router.post("/token")
async def login_for_access_token(
    patient:p_check,
    db:db_dependency
) -> Token:
    user = Auth.authenticate_user(patient,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = Auth.create_access_token(
        patient
    )
    return Token(access_token=access_token, token_type="bearer")



@router.get("/users/me/", response_model=p_check)
async def read_users_me(
    current_user: Annotated[p_check, Depends(Auth.get_current_active_user)]
):
    return current_user
