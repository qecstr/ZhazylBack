from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import null
from sqlalchemy.orm import Session
from app.models import Doctors
from app.schemas import doctors_json
from app.schemas import d_check
import app.OAuth2Config as Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
def get_Doctors_by_id(id:int,db:Session):
    return db.query(Doctors).filter(Doctors.id == id).first()
def checkByLogin(phone:int,db:Session):
    return  db.query(Doctors).filter(Doctors.phone == phone).first()


def get_Doctors(db:Session):
    return db.query(Doctors).all()

def register_Doctor(dj: doctors_json,db:Session):
    temp = Doctors(
        IIN = dj.IIN,
        phone = dj.phone,
        password = Auth.get_password_hash(dj.password),
        name = dj.name,
        surname = dj.surname,
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)


def update_Doctor(id:int, db:Session, dj: doctors_json):
    temp = get_Doctors_by_id(id,db)
    temp.email = dj.email
    temp.IIN = dj.IIN
    temp.login = dj.login
    temp.phone = dj.phone
    temp.password = dj.password
    temp.name = dj.name,
    temp.surname = dj.surname,
    temp.dateOfBirth = dj.dateOfBirth
    db.commit()
    db.refresh(temp)

def delete_Doctor(token:str,db:Session):
    phone = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM]).get("sub")
    id = checkByLogin(phone,db).id
    query = get_Doctors_by_id(id,db)
    db.delete(query)
    db.commit()


def isExist(d:d_check,db:Session):
    query = db.query(Doctors).filter(Doctors.login == d.login, Doctors.password == d.password).first()
    if (query == null):
        return False
    else:
        return True

def changePassword(login:int,newPassword:str,db:Session):
    query = db.query(Doctors).filter(Doctors.login == login).first()
    query.password = newPassword
    db.commit()
    db.refresh(query)


def authenticate_user(doctor:d_check,db:Session):
    user = checkByLogin(doctor.phone,db)
    if not user:
        return False
    if not Auth.verify_password(doctor.password, user.password):
        return False
    return user
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt