from sqlmodel import create_engine
import os

sqlite_filename = 'DB.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
db_url = f'sqlite:///{os.path.join(base_dir,sqlite_filename)}'
engine = create_engine(db_url, echo = True)