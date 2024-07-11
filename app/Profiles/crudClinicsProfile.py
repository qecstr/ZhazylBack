from sqlalchemy.orm import Session

from app.Profiles.ProfileModels import ClinicsProfile as Profile, ClinicsProfile
from app.schemas import ClinincsProfileJson as json
from app.Clinics import crud as userCrud
import app.OAuth2Config as Auth
def createClinicsProfile(json:json,db:Session):
    profile = Profile(
        name = json.name,
        address = json.address,
        phone = json.phone,
        services = json.services
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

def getClinicsProfileByName(name:str,db:Session):
    return db.query(ClinicsProfile).filter(ClinicsProfile.name == name).first()
def getClinicsProfileByUser(login:str,db:Session):
    id = userCrud.checkByLogin(login,db).id
    return db.query(ClinicsProfile).filter(ClinicsProfile.user_id == id).first()
def updateClinicsProfile(json:json,db:Session):
    profile = getClinicsProfileByName(json.name,db)
    profile.name = json.name
    profile.address = json.address
    profile.phone = json.phone
    profile.services = json.services
    db.commit()
    db.refresh(profile)

def deleteClinicsProfile(name:str,db:Session):
    profile = getClinicsProfileByName(name, db)
    db.delete(profile)
    db.commit()
def createWhenAuth(id:int,db:Session):

    profile = Profile(
        user_id = id
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
