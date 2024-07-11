from sqlalchemy import null
from sqlalchemy.orm import Session
from app.schemas import DoctorsProfileJson as Json
from app.Profiles.ProfileModels import DoctorsProfile as Profile
from app.schemas import doctors_json

def getByPhone(phone: int, db: Session):
    return db.query(Profile).filter(Profile.phone == phone).first()
def getById(id: int, db: Session):
    return db.query(Profile).filter(Profile.phone == id).first()

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


def update(Json: Json, db: Session, phone: int):
    temp = getByPhone(phone, db)
    temp.name=Json.name
    temp.surname=Json.surname
    temp.clinic = Json.clinic
    temp.experience = Json.experience
    temp.graphic = Json.graphic
    temp.payment = Json.payment
    db.commit()
    db.refresh(temp)


def delete(phone:int, db: Session):
    db.delete(getByPhone(phone, db))
    db.commit()
def createWhenAuth(doctors: doctors_json,db:Session,id:int):
    profile = Profile(
        name = doctors.name,
        surname = doctors.surname,
        IIN = doctors.IIN,
        phone = doctors.phone,
        user_id = id
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)