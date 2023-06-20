from fastapi import APIRouter, Depends, Path, status, Body, Query, HTTPException
from fastapi.responses import JSONResponse

from typing import List
from datetime import datetime

from app.models.user import User, UserCreate, UserUpdate
from app.models.response import ResponseModel
from app.config.db import get_session
from sqlmodel import Session, select

users_router = APIRouter()


@users_router.get(
        path='/users', 
        tags=['users'], 
        response_model=List[User], 
        status_code=status.HTTP_200_OK)
def get_users(offset: int = Query(description='Offset of the query',default=1,ge=1),
              limit: int = Query(description='Limit of data per request',default=100, lte=100), 
              session: Session = Depends(get_session)) -> List[User]:
    """
    Retrieves a list of users from the database with the given offset and limit. 

    Args:
        offset (int): Offset of the query. Default is 1.
        limit (int): Limit of data per request. Default is 100.
        session (Session): A database session object.

    Returns:
        List[User]: A list of User objects from the database.
    """
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@users_router.get(
        path='/user/{id}', 
        tags=['users'], 
        response_model=User, 
        status_code=status.HTTP_200_OK)
def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1), 
             session: Session = Depends(get_session)) -> User:
    """
    Retrieves a user object from the database by its ID.

    Args:
        id (int): The ID of the user to retrieve.
        session (Session): The database session to use.

    Returns:
        User: The user object associated with the given ID.

    Raises:
        HTTPException: If the user cannot be found in the database.
    """
    user = session.get(User, id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Error. User id:{id} Not found')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= {'message' : f'Error. User id:{id} Not found'})

@users_router.delete(
        path='/user/{id}', 
        tags=['users'], 
        response_model=ResponseModel, 
        status_code=status.HTTP_200_OK)
def delete_user(
    id:int = Path(description="User ID to delete",example=1,ge=1), 
    session: Session = Depends(get_session)) -> dict:
    """
    Deletes a user with the given id from the database if it exists.

    Args:
        id (int): User ID to delete, must be greater than or equal to 1.
        session (Session): A SQLAlchemy database session.

    Returns:
        dict: A JSON response containing a message indicating whether the user was deleted or not.
    """
    user = session.get(User, id)
    if user is not None:
        session.delete(user)
        session.commit()
        return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Error. User id:{id} Not found')

# @users_router.get('/users/', tags=['users'],response_model=List[User],status_code=status.HTTP_200_OK)
# def get_user_by_city(city:str = Query(description='look for City',example='Neiva', min_length=2,max_length=20)) -> List[User]:
#     data = [user for user in users if user['city'] == city]
#     if len(data)==0:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=data) #Not Found
#     else:
#         return JSONResponse(status_code=status.HTTP_200_OK,content=data) #Not Found

@users_router.post(
        path='/user', 
        tags=['users'],
        response_model=User, 
        status_code=status.HTTP_201_CREATED)
def create_user(
    user:UserCreate = Body(...), 
    session: Session = Depends(get_session)) -> dict:
    """
    Creates a new user in the database with the given user data.
    
    Args:
        user: A UserCreate instance containing the data for the new user.
        session: A SQLAlchemy Session instance to use for the database transaction.
        
    Returns:
        A JSONResponse instance containing a success message, the ID of the created user, and the username of the created user.
    """
    user_db = User.from_orm(user)
    user_db.initDate = datetime.now()
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message' : 'User added', 'id' : user_db.id, 'username' : user_db.name })

@users_router.put(
        path='/user/{id}', 
        tags=['users'],
        response_model=ResponseModel, 
        status_code=status.HTTP_200_OK)
def update_user(
    id:int = Path(description="User ID to modify",example=1,ge=1), 
    user:UserUpdate = Body(), 
    session: Session = Depends(get_session)) -> dict:
    """
    Updates a user with the given ID in the database with the provided new data. 
    
    Args:
        id (int): User ID to modify. Must be greater than or equal to 1.
        user (UserUpdate): The updated user data to replace the existing data.
        session (Session): A SQLAlchemy session dependency.
        
    Returns:
        dict: A JSON response containing a message indicating whether the update was successful or not.
    Raises:
        HTTPException: If the user with the given ID is not found in the database.
    """
    user_db = session.get(User,id)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Error. User id:{id} Not found')
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db,key,value)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return JSONResponse(content={'message':f'User id:{id} updated correctly'},status_code=status.HTTP_200_OK)
