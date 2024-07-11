from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends,  HTTPException, status
from app.database import SessionLocal
from typing import Annotated
from app.Clinics import crud as crudClinics
from app.adminPanel import crud
from jose import JWTError, jwt
from app.schemas import TokenDataForAdmins as TokenData, Token
from app.schemas import AdminJson
from app.schemas import ClinicsJson
from app.Profiles import crudClinicsProfile
import app.OAuth2Config as Auth
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    admin = crud.get_admin(token_data,db)
    if admin is None:
        raise credentials_exception
    return admin

async def get_current_active_admin(
    current_admin: Annotated[AdminJson, Depends(get_current_admin)]
):
    if current_admin.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_admin
@router.get("/clinics/checkToken/{token}")
async def check_token(token:str,
                      db:db_dependency,
                      current_admin: Annotated[AdminJson, Depends(get_current_active_admin)]):
    return crudClinics.check_token(token,db,current_admin.password)
@router.post("/clinics/create/{token}")
async def create_clinic(token:str,
                      db:db_dependency,
                      current_admin: Annotated[AdminJson, Depends(get_current_active_admin)],
                        json:ClinicsJson):
    isAuth = crudClinics.check_token(token,db,current_admin.password)
    if not isAuth:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    else:
        crudClinics.create_clinic(json,db)
        login = Auth.decode_access_token(token)
        id = crudClinics.checkByLogin(login,db)
        crudClinicsProfile.createWhenAuth(id,db)

@router.delete("/clinics/delete/{token}")
async def delete_clinic(token:str,
                      db:db_dependency,
                      current_admin: Annotated[AdminJson, Depends(get_current_active_admin)],
                      login:str):
    isAuth = crudClinics.check_token(token, db, current_admin.password)
    if not isAuth:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        crudClinics.delete_clinic(login,db)



async def get_current_clinic(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    admin = crudClinics.checkByLogin(token_data.username,db)
    if admin is None:
        raise credentials_exception
    return admin

async def get_current_active_clinic(
    current_clinic: Annotated[ClinicsJson, Depends(get_current_admin)]
):

    return current_clinic

@router.post("/clinic/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:db_dependency
) -> Token:
    json = ClinicsJson(login  = form_data.username, password = form_data.password)
    clinic = crudClinics.authenticate_user(json,db)
    if not clinic:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crudClinics.create_access_token(
        data={"sub": clinic.login})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/clinic/me/", response_model=ClinicsJson)
async def read_users_me(

    current_clinic: Annotated[ClinicsJson, Depends(get_current_active_clinic)],

):
    return current_clinic