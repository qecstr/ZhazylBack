from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.security import OAuth2PasswordBearer
from app.schemas import Token
from app.database import SessionLocal

from typing import Annotated
from app import OAuth2Config as Auth
from app.schemas import AdminJson
from app.adminPanel import crud

from app.schemas import TokenDataForAdmins as TokenData
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from fastapi import Depends,  HTTPException, status

from sqlalchemy.orm import Session
admin = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/token")
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
@admin.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:db_dependency
) -> Token:
    json = AdminJson(login  = form_data.username, password = form_data.password)
    admin= Auth.authenticate_Admin(json,db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Auth.create_access_token_for_admin(
        data={"sub": admin.login})
    return Token(access_token=access_token, token_type="bearer")

@admin.get("/admin/me/", response_model=AdminJson)
async def read_users_me(

    current_admin: Annotated[AdminJson, Depends(get_current_active_admin)],

):
    return current_admin


@admin.post("/admin/create")
async def create_admin(json: AdminJson,db:db_dependency):
    crud.create_Admin(json,db)


