import datetime
from typing import ClassVar, Generic, Optional, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic.v1.generics import GenericModel
from sqlalchemy import Integer

T = TypeVar('T')
class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class patients_json(BaseModel):
    INN :int
    phone : int
    login : str
    email : str
    password : str
    name : str
    surname : str
    dateOfBirth : datetime.date

class p_check(BaseModel):
    login: str
    password: str
class doctors_json(BaseModel):
    IIN : int
    phone : int
    login : str
    email : str
    password : str
    name : str
    surname : str
    email_confirmation : str

class d_check(BaseModel):
    login: str
    password: str
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]