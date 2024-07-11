from app.database import Base
from sqlalchemy import types, ForeignKey
from sqlalchemy import Column,Integer



class Services(Base):
    __tablename__ = 'services'
    id = Column(Integer,primary_key=True,index = True)
    name = Column(types.TEXT,index=True)
    price = Column(types.DOUBLE_PRECISION,index=True)
    sale = Column(types.DOUBLE_PRECISION,index=True,default=0)
    time = Column(types.Time,index=True)
    clinic_id = Column(Integer,index = True)
    doctor_id = Column(Integer,index = True,default=0)

