import json

from httpx import AsyncClient
import requests
from app.schemas import patients_json, Response
from fastapi import APIRouter
from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import doctors_json
from app.schemas import p_check
from app.schemas import d_check

from app.Doctors import crud as d_crud
from app.Patients import crud as p_crud

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

@router.post("/patients/changePassword/{login}/{newPassword}")
async def changePatientsPassword(login: str,newPassword:str,db: db_dependency):
    p_crud.changePassword(login,newPassword,db)

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
async def changePatientsPassword(login: str,newPassword:str,db: db_dependency):
    d_crud.changePassword(login,newPassword,db)



#не рабочее

API = "196545763551645"
URL = "https://graph.facebook.com/v18.0/237284509471319/messages"
client = AsyncClient()

@router.get("/sendMesage")
async def sendMessage():
    temp = {"name": "hello_world",
            "language": {
                "code": "en_US"
            }}

    data = {
    "messaging_product": "whatsapp",
    "to": "787718186663",
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

    print(json.dumps(data, indent=4))
    t = json.dumps(data)
    print(data)
    headers = {"Authorization": "EAATZCc3Y9atgBOwU7ioPjdXWklOYqoN6p3kIUYhcySS739cIIVtBOedzgxf7Ii9fS05OU6aoNWAcVwZBCWxQyyBaAh3KDLzqepMmA5WcFnCP9oa75gYKFuDmGqnOZATwDPI6CLI9lu7QHBTFXBPBFsTUi9GH9nslOgZBjJZChcK1bbj5Y0PSPy4SZBiXBZB8SdvhpiFM8W51aZABmR1vNAcAMYj8jPkZD"}
    return requests.post(url=URL,data=t,headers=headers).json()


