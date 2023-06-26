# SQLModel
from sqlmodel import SQLModel, Field
# Python
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime
from pydantic import SecretStr, EmailStr

class UserBase(SQLModel):
    name  : str = Field(min_length=3, max_length=50)
    email : EmailStr = Field(unique=True)
    city : Optional[str] = None
    country : Optional[str] = None

class User(UserBase, table=True):
    user_id : UUID = Field(default_factory=uuid4,
                           primary_key=True,
                           index=True,
                           nullable=False)
    pass_hash : str
    initDate : datetime = Field(default_factory=datetime.now)
    userType : str = Field(default='user')
    idTelegram : Optional[int] = None

class UserCreate(UserBase):
    password : SecretStr = Field(min_length=8, max_length=50)
    class Config:
        schema_extra = {
            'example': {
                'name'      : 'Example Herrera',
                'email'     : 'user@example.com',
                'password'  : 'MyPassword',
                'city'      : 'City of User [Optional]',
            }
        }

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
