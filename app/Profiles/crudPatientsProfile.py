from sqlalchemy import null
from sqlalchemy.orm import Session
from app.schemas import PatienceProfileJson as Json
from app.Profiles.ProfileModels import PatientsProfile as Profile


def getById(id:int,db:Session):
    return db.query(Profile).filter(Profile.id == id).first()
def create(Json:Json,db:Session):
    temp = Profile(IIN = Json.INN,
                   phone = Json.phone,
                   name = Json.name,
                   surname = Json.surname,
                   dateOfBirth = Json.dateOfBirth,
                   sex = Json.sex
                   )
    db.add(temp)
    db.commit()
    db.refresh(temp)

def update(Json:Json,db:Session,id:int):
    temp = getById(id,db)
    temp.IIN=Json.INN
    temp.phone=Json.phone
    temp.name=Json.name
    temp.surname=Json.surname
    temp.dateOfBirth=Json.dateOfBirth
    temp.sex=Json.sex
    db.commit()
    db.refresh(temp)

def delete(id:int,db:Session):
    db.delete(getById(id,db))
    db.commit()
