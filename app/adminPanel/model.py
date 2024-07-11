from app.database import Base
from sqlalchemy import types, ForeignKey
from sqlalchemy import Column,Integer

class AdminModel(Base):
    __tablename__ = 'AdminModel'
    id = Column(types.Integer, primary_key=True)
    login = Column(types.TEXT,index = True,unique=True)
    password = Column(types.TEXT,index = True)