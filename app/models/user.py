from config.database import engine
from sqlmodel import SQLModel, Field
from typing import Optional

class Users(SQLModel):
    # __tablename__='users'
    id: Optional[int] = Field(default=None, primary_key=True)
    name  : str = Field(min_length=3, max_length=50)
    email : str = Field(min_length=10, max_length=50)
    city  : str = Field(min_length=3, max_length=50)
    initDate : Optional[str] = None

def create_db_table():
    SQLModel.metadata.create_all(engine)