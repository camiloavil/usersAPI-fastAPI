# SQLModel
from sqlmodel import SQLModel, Field
# Python
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    name  : str = Field(min_length=3, max_length=50)
    email : str = Field(unique=True, min_length=10, max_length=50)

class User(UserBase, table=True):
    user_id : UUID = Field(default_factory=uuid4,
                           primary_key=True,
                           index=True,
                           nullable=False)
    pass_hash : str
    initDate : datetime = Field(default_factory=datetime.now)
    userType : str = Field(default='user')
    city : Optional[str] = None
    idTelegram : Optional[int] = None
    # city  : str = Field(min_length=3, max_length=50)
    # id: Optional[int] = Field(default=None, primary_key=True)

class UserFB(UserBase):
    user_id : UUID
    initDate : datetime
    city : Optional[str] = None
    idTelegram : Optional[int] = None
    class Config:
        schema_extra = {
            'example': {
                'name'      : 'Name of User',
                'email'     : 'email of User',
                'user_id'   : 'id of User'
            }
        }

class UserCreate(UserBase):
    class Config:
        schema_extra = {
            'example': {
                'name' : 'Nombre',
                'email' : 'user@example.com',
                'city' : 'Ciudad'
            }
        }

class UserUpdate(SQLModel):
    name  : Optional[str] = None 
    email : Optional[str] = None 
    city  : Optional[str] = None
    class Config:
        schema_extra = {
            'example': {
                'name' : 'Nombre',
                'email' : 'user@example.com',
                'city' : 'Ciudad'
            }
        }
