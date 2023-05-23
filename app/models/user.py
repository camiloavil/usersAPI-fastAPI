from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    name  : str = Field(min_length=3, max_length=50)
    email : str = Field(index=True, min_length=10, max_length=50)
    city  : str = Field(min_length=3, max_length=50)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    initDate : Optional[datetime] = None

class UserRead(UserBase):
    id: int
    initDate: datetime

class UserCreate(UserBase):
    class Config:
        schema_extra = {
            'example': {
                'name' : 'Nombre',
                'email' : 'user@example.com',
                'city' : 'Ciudad'
            }
        }

class UserUpdate(UserBase):
    pass