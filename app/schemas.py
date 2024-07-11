import datetime
from typing import ClassVar, Generic, Optional, TypeVar, Union

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
    password : str
    name : str
    surname : str

class p_check(BaseModel):
    phone: int
    password: str
class doctors_json(BaseModel):
    IIN : int
    phone : int
    password : str
    name : str
    surname : str

class d_check(BaseModel):
    phone: int
    password: str
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class Number(BaseModel):
    number: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone: Union[str, None] = None

class TokenDataForAdmins(BaseModel):
    username: Union[str, None] = None
class changePass(BaseModel):
    phone: int
    password: str
    newPassword: str

class PatienceProfileJson(BaseModel):
    phone: int
    INN: int
    name: str
    surname: str
    dateOfBirth: datetime
    sex: str

class DoctorsProfileJson(BaseModel):
    name: str
    surname: str
    clinic: str
    experience: str
    graphic: str
    payment: str


class ServiceJson(BaseModel):
    name: str
    price: float
    sale: Optional[float]
    time: datetime.time
    clinic_id: int
    doctor_id: Optional[int]

class OrdersJson(BaseModel):
    users_phone: int
    service_name: str
    clinics_name: str
    time: datetime.time
    date: datetime.date
    doctor_id: Optional[int]


class AdminJson(BaseModel):
    login: str
    password: str
    disabled: Optional[bool] = None

class ClinicsJson(BaseModel):
    login: str
    password: str

class ClinincsProfileJson(BaseModel):
    name: str
    address: str
    phone: str
    services: str

class offerBoardJson(BaseModel):
    text: str
    worktime: str
    phone: int