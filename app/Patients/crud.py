from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import null
from sqlalchemy.orm import Session
from app.models import Patients
from app.schemas import patients_json
from app.schemas import p_check
from app.schemas import changePass
import app.OAuth2Config as Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
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

def checkByLogin(phone:int,db:Session):
    return  db.query(Patients).filter(Patients.phone == phone).first()


def changePassword(login:int,new_password:str,db:Session):
    query = db.query(Patients).filter(Patients.phone == login).first()
    query.password =new_password
    db.commit()
    db.refresh(query)

def authenticate_user(patient:p_check,db:Session):
    user = checkByLogin(patient.phone,db)
    if not user:
        return False
    if not Auth.verify_password(patient.password, user.password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
