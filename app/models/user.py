from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name  : str = Field(min_length=3, max_length=50)
    email : str = Field(min_length=10, max_length=50)
    city  : str = Field(min_length=3, max_length=50)
    initDate : Optional[datetime] = None
