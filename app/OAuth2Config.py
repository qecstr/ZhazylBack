
from typing import Annotated

from app.database import SessionLocal
from app.models import Patients
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from app.Patients.crud import checkByLogin
from app.schemas import p_check
from app.Patients.crud import isExist as isExist
from sqlalchemy.orm import Session
from app.schemas import AdminJson
from app.adminPanel.model import AdminModel
from app.adminPanel.crud import check_admin, get_admin
from app.adminPanel.route import db_dependency
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_Admin(adminJson:AdminJson,db:Session):
    temp = check_admin(adminJson, db)
    admin = AdminJson(login=temp.login,password=temp.password)
    if not admin:
        return False
    if not verify_password(adminJson.password, admin.password):
        return False
    return admin




def create_access_token_for_admin(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def decode_access_token(token:str):

    encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return encoded_jwt.get("sub")