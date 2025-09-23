from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, time

class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    phone: str
    country: str
    address: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PropertyClaim(BaseModel):
    policy_num: str
    ph_num: str
    staff_id: Optional[str] = None
    inc_date: date
    inc_time: str
    address: str
    property_type: str
    damage_type: str
    country: str
    emg_cont: Optional[str] = None
    descr: str

class MotorClaim(BaseModel):
    policy_num: str
    ph_num: str
    staff_id: Optional[str] = None
    inc_date: date
    inc_time: str
    plate_no: str
    colour: str
    engine_no: Optional[str] = None
    chasis_no: Optional[str] = None
    km_reading: Optional[str] = None
    variant_year: str
    address: str
    country: str
    descr: str

class SupportTicket(BaseModel):
    name: str
    email: str
    phone: str
    policy: Optional[str] = None
    subject: str
    priority: str
    message: str
    