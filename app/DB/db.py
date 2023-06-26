# APP
from app.models.user import SQLModel, User
from sqlmodel import Session, create_engine, select
# Python
import os

sqlite_filename = 'DB.sqlite'                       #Filename of sqlite DB
base_dir = os.path.dirname(os.path.realpath(__file__))
db_url = f'sqlite:///{os.path.join(base_dir,sqlite_filename)}' #set location of DB File on the same folder of this file
engine = create_engine(db_url, echo = False)         #echo =True set verbose entire DB process

def create_db_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def get_userDB_by_email(username: str):
    """
    Retrieves a user's database object by their email address.

    :param username: A string representing the email address of the user.
    :type username: str

    :return: The database object representing the user.
    :rtype: User
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == username)
        user_db = session.exec(statement).first()
    return user_db