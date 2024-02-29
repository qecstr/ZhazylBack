from sqlalchemy import null
from sqlalchemy.orm import Session
from app.models import Doctors
from app.schemas import doctors_json
from app.schemas import d_check
def get_Doctors_by_id(id:int,db:Session):
    return db.query(Doctors).filter(Doctors.id == id).first()

def get_Doctors(db:Session):
    return db.query(Doctors).all()

def register_Doctor(dj: doctors_json,db:Session):
    temp = Doctors(
        IIN = dj.IIN,
        phone = dj.phone,
        login = dj.login,
        email = dj.email,
        password = dj.password,
        name = dj.name,
        surname = dj.surname,
        dateOfBirth = dj.dateOfBirth
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)


def update_Doctor(id:int, db:Session, dj: doctors_json):
    temp = get_Doctors_by_id(id,db)
    temp.email = dj.email
    temp.IIN = dj.IIN
    temp.login = dj.login
    temp.phone = dj.phone
    temp.password = dj.password
    temp.name = dj.name,
    temp.surname = dj.surname,
    temp.dateOfBirth = dj.dateOfBirth
    db.commit()
    db.refresh(temp)

def delete_Doctor(id:int,db:Session):
    query = get_Doctors_by_id(id,db)
    db.delete(query)
    db.commit()


def isExist(d:d_check,db:Session):
    query = db.query(Doctors).filter(Doctors.login == d.login, Doctors.password == d.password).first()
    if (query == null):
        return False
    else:
        return True

def changePassword(login:str,newPassword:str,db:Session):
    query = db.query(Doctors).filter(Doctors.login == login).first()
    query.password = newPassword
    db.commit()
    db.refresh(query)