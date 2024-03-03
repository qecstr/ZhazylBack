from sqlalchemy import null
from sqlalchemy.orm import Session
from app.models import Patients
from app.schemas import patients_json
from app.schemas import p_check
from app.schemas import changePass
import app.OAuth2Config as Auth
def get_Patients_by_id(id:int,db:Session):
    return db.query(Patients).filter(Patients.id == id).first()

def get_Patients(db:Session):
    return db.query(Patients).all()

def register_Patient(pj: patients_json, db:Session):
    temp = Patients(
        INN = pj.INN,
        phone = pj.phone,
        password = Auth.get_password_hash(pj.password),
        name = pj.name,
        surname = pj.surname,
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)


def update_Patient(id:int, db:Session, pj: patients_json):
    temp = get_Patients_by_id(id,db)
    temp.IIN = pj.IIN
    temp.phone = pj.phone
    temp.password = pj.password
    temp.name = pj.name,
    temp.surname = pj.surname,
    db.commit()
    db.refresh(temp)

def delete_Patient(id:int,db:Session):
    query = get_Patients_by_id(id,db)
    db.delete(query)
    db.commit()
def isExist(p:p_check,db:Session):
    query = db.query(Patients).filter(Patients.phone == p.phone, Patients.password == p.password).first()
    if (query == null):
        return False
    else:
        return True

def checkByLogin(phone:str,db:Session):
    return  db.query(Patients).filter(Patients.phone == phone).first()


def changePassword(temp:changePass,db:Session):
    query = db.query(Patients).filter(Patients.phone == temp.phone).first()
    query.password = temp.newPassword
    db.commit()
    db.refresh(query)


