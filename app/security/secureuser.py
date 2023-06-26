# FastAPI
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
# PassLib
from passlib import CryptContext
# Jose
from jose import jwt, JWTError
# APP
from app.security import URL_USER_LOGIN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_User_scheme = OAuth2PasswordBearer(tokenUrl=URL_USER_LOGIN)

secure_user = APIRouter()

def verify_password(plain_password: str, hashed_password: str):
    """
    Verify if a given plain password matches a hashed password using the PyJWT password context.

    :param plain_password: A string representing the plain password to be verified.
    :type plain_password: str
    :param hashed_password: A string representing the hashed password to compare with.
    :type hashed_password: str
    :return: A boolean indicating if the plain password matches the hashed password.
    :rtype: bool
    """
    return pwd_context.verify(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str):
    """
    Generates a hash of the input string password using the password hashing framework 
    pwd_context. 

    :param password: The password string to hash.
    :type password: str
    :return: Hashed password string.
    :rtype: str
    """
    return pwd_context.hash(password.encode('utf-8'))