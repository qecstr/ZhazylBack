
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import offerBoardJson
from app.offerBoard import crud
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/offer/add/{clinic_token}")
async def create_offer(offer: offerBoardJson, db:db_dependency,clinic_token:str):
    crud.create_offer(offer,db,clinic_token)

