from app.database import Base
from sqlalchemy import types, ForeignKey
from sqlalchemy import Column,Integer

class OfferBoard(Base):
    __tablename__ = 'OfferBoard'
    id = Column(Integer, primary_key=True)
    clinic_name = Column(types.TEXT,index = True)
    address = Column(types.TEXT,index=True)
    worktime = Column(types.TEXT,index=True)
    phone = Column(Integer,index=True)
    text = Column(types.TEXT,index=True)
    clinic_id = Column(Integer,index=True)

