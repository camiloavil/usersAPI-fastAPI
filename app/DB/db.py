# APP
from app.models.user import SQLModel, User
# SQLModel
from sqlmodel import Session, create_engine, select
from sqlalchemy.exc import IntegrityError
# Python
import os

#Filename of sqlite DB
SQLITE_FILENAME = 'DB.sqlite'                       
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


#set location of DB File on the same folder of this file
DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR,SQLITE_FILENAME)}' 
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

#echo =True set verbose entire DB process
engine = create_engine(DATABASE_URL, echo = False)         

def create_db_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def add_user_to_db(user: User):
    """
    Add a user to the database.

    Parameters:
    - user: An instance of the User class.

    Returns:
    - The added user if successful, None otherwise.
    """
    try:
        with Session(engine) as session:
            session.add(user)
            session.commit()
        return user
    except IntegrityError as e:
        print(e)
    except Exception as e:
        print("Error Creating User:"+str(e))
    return None

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