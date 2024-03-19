from sqlalchemy import null
from sqlalchemy.orm import Session
from app.schemas import DoctorsProfileJson as Json
from app.Profiles.ProfileModels import DoctorsProfile as Profile


def getById(id: int, db: Session):
    return db.query(Profile).filter(Profile.id == id).first()


def create(Json: Json, db: Session):
    temp = Profile(name=Json.name,
                   surname=Json.surname,
                   clinic = Json.clinic,
                   experience = Json.experience,
                   graphic = Json.graphic,
                   payment = Json.payment
                   )
    db.add(temp)
    db.commit()
    db.refresh(temp)


def update(Json: Json, db: Session, id: int):
    temp = getById(id, db)
    temp.name=Json.name
    temp.surname=Json.surname
    temp.clinic = Json.clinic
    temp.experience = Json.experience
    temp.graphic = Json.graphic
    temp.payment = Json.payment
    db.commit()
    db.refresh(temp)


def delete(id: int, db: Session):
    db.delete(getById(id, db))
    db.commit()
