from app.models.user import SQLModel        #loading model user
from sqlmodel import create_engine
import os

sqlite_filename = 'DB.sqlite'                       #Filename of sqlite DB
base_dir = os.path.dirname(os.path.realpath(__file__))
db_url = f'sqlite:///{os.path.join(base_dir,sqlite_filename)}' #set location of DB File on the same folder of this file
engine = create_engine(db_url, echo = True)         #echo =True set verbose entire DB process

def create_db_table():
    SQLModel.metadata.create_all(engine)