from sqlalchemy.orm import Session
from app.services.models import Services
from app.schemas import ServiceJson

def getById(db: Session, id: int):
    return db.query(Services).filter(Services.id == id).first()

def createService(json:ServiceJson,db: Session):
    service = Services(
        name=json.name,
        price = json.price,
        sale = json.sale,
        time = json.time,
        clinic_id = json.clinic_id,
        doctor_id = json.doctor_id

    )
    db.add(service)
    db.commit()
    db.refresh(service)

def updateService(json:ServiceJson,db: Session,id:int):
    service = getById(db,id)
    service.name = json.name
    service.price = json.price
    service.sale = json.sale
    service.time = json.time
    service.clinic_id =json.clinic_id
    service.doctor_id = json.doctor_id
    db.commit()
    db.refresh(service)

def deleteService(db:Session,id:int):
    service = getById(db,id)
    db.delete(service)
    db.commit()

def getAllServices(db: Session, clinic_id:int):
    return db.query(Services).filter(Services.clinic_id == clinic_id).all()

def setDoctorId(db: Session, doctor_id:int, service_id:int):
    service = getById(db,service_id)
    service.doctor_id = doctor_id
    db.commit()
    db.refresh(service)

def getByNameAndId(db:Session, name:str, id:int):
    return db.query(Services).filter(Services.name ==name,Services.clinic_id == id).first()