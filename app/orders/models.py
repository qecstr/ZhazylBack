from app.database import Base
from sqlalchemy import types, ForeignKey
from sqlalchemy import Column,Integer

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True,index=True)
    users_phone = Column(Integer,index=True)
    service_name = Column(types.TEXT,index=True)
    clinics_name = Column(types.TEXT,index=True)
    time = Column(types.TIME,index=True)
    date = Column(types.DATE,index = True)
    price = Column(types.DOUBLE_PRECISION,index=True)
    sale = Column(types.DOUBLE_PRECISION,index=True)
    results = Column(types.TEXT,index=True,nullable=True)
    users_id = Column(Integer,index=True)
    clinic_id = Column(Integer,index=True)
    doctor_id = Column(Integer,index = True,default=0)
    order_id = Column(Integer,index=True,default=0)
#подвтеждение

