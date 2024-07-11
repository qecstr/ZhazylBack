from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from app.models import Clinics
from app.schemas import ClinicsJson
from app.adminPanel.model import AdminModel
import app.OAuth2Config as Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def check_token(token:str,db:Session,password_hash:str):
    login = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]).get('sub')
    admin = db.query(AdminModel).filter(AdminModel.login == login,AdminModel.password==password_hash).first()
    if admin is None :
        return False
    else:
        return True
def checkByLogin(login:str,db:Session):
    return db.query(Clinics).filter(Clinics.login == login).first()

def create_clinic(json: ClinicsJson,db:Session):
    clinic = Clinics(
        login = json.login
        ,password = json.password
    )
    db.add(clinic)
    db.commit()
    db.refresh(clinic)
def delete_clinic(login:str,db:Session):
    clinic = db.query(Clinics.login == login).first()
    db.delete(clinic)
    db.commit()

def authenticate_user(clinic:ClinicsJson,db:Session):
    user = checkByLogin(clinic.phone,db)
    if not user:
        return False
    if not Auth.verify_password(clinic.password, user.password):
        return False
    return user
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
