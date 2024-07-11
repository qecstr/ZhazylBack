from sqlalchemy.orm import Session
from app.Profiles.crudClinicsProfile import getClinicsProfileByName
from app.services.crudServices import getByNameAndId
from app.orders.models import Orders
from app.schemas import OrdersJson
from app.Profiles.crudPatientsProfile import getPatientbyPhone
import app.OAuth2Config as Auth
from app.Doctors import crud as crudDoctors
from app.Clinics import crud as crudClinics
from random import randint
def getById(id:int, db:Session):
    return db.query(Orders).filter(Orders.id == id).fisrt()
def create_order(order:OrdersJson,db: Session):
    clinic = getClinicsProfileByName(order.clinics_name,db)
    service = getByNameAndId(db,order.service_name,clinic.id)
    order = Orders(
        users_phone = order.users_phone,
        service_name = order.service_name,
        clinics_name = order.clinics_name,
        time = order.time,
        date = order.date,
        price = service.price,
        sale = service.sale,
        users_id = getPatientbyPhone(order.users_phone,db),
        clinics_id = clinic.id,
        order_id = generate_randomOrderId()
    )
    db.add(order)
    db.commit()
    db.refresh(order)


def setDoctorsId(doctors_id:int,db: Session,id:int):
   temp =  getById(id,db)
   temp.doctors_id = doctors_id
   db.commit()
   db.refresh(temp)

def getAllPatinetsOrders(db:Session,token:str):
    phone = Auth.decode_access_token(token)
    return db.query(Orders).filter(Orders.users_phone == phone).all()
def getAllDoctorsOrders(db:Session,token:str):
    phone = Auth.decode_access_token(token)
    doctors_id = crudDoctors.checkByLogin(phone,db).id
    return db.query(Orders).filter(Orders.doctor_id == doctors_id).all()
def getAllClinicsOrders(db:Session,token:str):
    login = Auth.decode_access_token(token)
    clinics_id = crudClinics.checkByLogin(login, db).id
    return db.query(Orders).filter(Orders.clinic_id == clinics_id).all()

def generate_randomOrderId():
    range_start = 10 ** (6 - 1)
    range_end = (10 ** 6) - 1
    return randint(range_start, range_end)
