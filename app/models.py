from app.database import Base
from sqlalchemy import types
from sqlalchemy import Column,Integer


class Patients(Base):
    __tablename__ = 'Patients'

    id = Column(Integer, primary_key=True,index=True)
    INN = Column(Integer,index=True,unique=True)
    phone = Column(types.VARCHAR,index=True,unique=True)
    password = Column(types.TEXT,index=True)
    name = Column(types.TEXT,index = True)
    surname = Column(types.TEXT,index=True)



class Doctors(Base):
    __tablename__ = 'Doctors'

    id = Column(Integer, primary_key=True,index=True)
    INN = Column(Integer,index=True,unique=True)
    phone = Column(types.VARCHAR,index=True,unique=True)
    password = Column(types.TEXT,index=True)
    name = Column(types.TEXT,index = True)
    surname = Column(types.TEXT,index=True)
class Clinics(Base):
    __tablename__ = 'Clinics'
    id = Column(Integer, primary_key=True,index=True)
    login = Column(types.VARCHAR,index=True)
    password = Column(types.TEXT,index=True)




