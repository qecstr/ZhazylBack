
from app.database import Base
from sqlalchemy import types
from sqlalchemy import Column,Integer






class PatientsProfile(Base):
    __tablename__ = 'PatientsProfile'

    id = Column(Integer, primary_key=True,index=True)
    INN = Column(Integer,index=True,unique=True)
    phone = Column(types.VARCHAR,index=True,unique=True)
    name = Column(types.TEXT,index = True)
    surname = Column(types.TEXT,index=True)
    dateOfBirth = Column(types.DATE, index=True)
    sex = Column(types.TEXT, index=True)
    user_id = Column(Integer,index = True)



class DoctorsProfile(Base):
    __tablename__ = 'DoctorsProfile'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(types.TEXT,index = True)
    surname = Column(types.TEXT,index=True)
    clinic = Column(types.TEXT, index=True)
    experience = Column(types.TEXT, index=True)
    graphic = Column(types.TEXT,index = True)
    payment = Column(types.TEXT, index=True)
    user_id = Column(Integer,index = True)

class ClinicsProfile(Base):
    __tablename__ = 'ClinicsProfile'
    id = Column(Integer, primary_key=True)
    name = Column(types.TEXT,index=True)
    address = Column(types.TEXT,index=True)
    phone = Column(types.VARCHAR,index=True)
    services = Column(types.TEXT,index=True)
    user_id = Column(Integer, index=True)




