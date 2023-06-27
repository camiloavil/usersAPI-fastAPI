#FastAPI
from fastapi import APIRouter, status, HTTPException
from fastapi import Depends, Body, Query, Form, Path
from fastapi.responses import JSONResponse
# SQLModel
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
#Python
from typing import Annotated, List
# APP
from app.models.user import User, UserCreate, UserUpdate, UserFB
from app.models.response import ResponseModel
from app.DB.db import get_session
from app.security.secureuser import verify_password, get_password_hash, get_current_user

users_router = APIRouter()

@users_router.get('/users', tags=['users'], 
                  response_model=List[User], 
                  status_code=status.HTTP_200_OK
                )
def get_users(offset: int = Query(description='Offset of the query',default=1,ge=1),
              limit: int = Query(description='Limit of data per request',default=100, lte=100), 
              session: Session = Depends(get_session)) -> List[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@users_router.get(path='/user/{id}', 
                  tags=['users'], 
                  response_model=User, 
                  status_code=status.HTTP_200_OK)
def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1), 
             session: Session = Depends(get_session)) -> User:
    """
    Retrieves a user by their ID. 
    
    Args:
        id (int): ID of the user to retrieve. Must be greater than or equal to 1.
        session (Session): A SQLAlchemy Database Session dependency.

    Returns:
        User: A Pydantic User model representing the retrieved user.
        JSONResponse (status_code=404): A JSON response containing an error message if the user is not found.
    """
    user = session.get(User, id)
    if user is not None:
        return user
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= {'message' : f'Error. User id:{id} Not found'})

@users_router.post(path='/user', 
                   tags=['Users'],
                   response_model=UserFB, 
                   status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate = Body(), 
                session: Session = Depends(get_session)) -> dict:
    """
    Creates a new user and adds it to the database. Accepts a user object as a Body parameter in the request. 
    The function returns a dictionary representation of the newly created user
    If the user already exists, it raises an HTTPException with a status code of 409. 
    If there is an internal error while creating the user, it raises an HTTPException with a status code of 400. 

    :param user: UserCreate object. Required. 
    :param session: Session object. Required.
    :return: A dictionary representation of the newly created user
    :raises HTTPException 409: If the user already exists.
    :raises HTTPException 400: If there is an internal error while creating the user.
    """
    userDict = user.dict()
    userDict.update({'pass_hash' : get_password_hash(user.password.get_secret_value())})

    try:
        user_db = User.from_orm(User(**userDict))
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        print(str(user_db))
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    except Exception as e:
        print("Error Creating User:"+str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Internal Error")
    return UserFB(**user_db.dict())

@users_router.get(path="/myuser",
                  response_model=UserFB,
                  tags=["Users"])
async def info_User(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get information about the current user.

    :return: UserFB - Information about the current user
    """
    return UserFB(**current_user.dict())

# @users_router.put(path='/myuser/{id}', tags=['users'],response_model=ResponseModel, status_code=status.HTTP_200_OK)
@users_router.put(path='/myuser', 
                  tags=['Users'],
                  response_model= UserFB, 
                  status_code=status.HTTP_200_OK)
def update_user(current_user: Annotated[User, Depends(get_current_user)],
                newData: UserUpdate = Body(),
                session: Session = Depends(get_session)) -> dict:
    """
    Updates the user information for the user with the given user ID. 

    Args:
        current_user (Annotated[User, Depends(get_current_user)]): The user making the request.
        newData (UserUpdate = Body()): The new user information to update.

    Returns:
        A dictionary containing the updated user information.
    """
    newData_dict = newData.dict(exclude_unset=True)
    user_db = session.get(User,current_user.user_id)
    for key, value in newData_dict.items():
        print(f'key:{key} value:{value}')
        setattr(user_db,key,value)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return UserFB(**user_db.dict())
    return JSONResponse(content={'message':f'User id:{id} updated correctly'},status_code=status.HTTP_200_OK)

@users_router.delete(path='/myuser', 
                     tags=['Users'], 
                     response_model=dict, 
                     status_code=status.HTTP_200_OK)
def disable_user(current_user: Annotated[User, Depends(get_current_user)],
                session: Session = Depends(get_session)) -> dict:
    """
    Deletes a user from the database by setting their 'is_active' attribute to False.
    
    Args:
        current_user (Annotated[User, Depends(get_current_user)]): The current user making the request.
        session (Session, optional): The SQLAlchemy session object. Defaults to Depends(get_session).
        
    Returns:
        dict: A JSON response containing a message indicating the user was deleted, and a 200 HTTP status code.
    """
    user_db = session.get(User, current_user.user_id)
    setattr(user_db,'is_active',False)
    session.commit()
    return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)


# @users_router.delete(path='/user/{id}', 
#                      tags=['AdminUsers'], 
#                      response_model=ResponseModel, 
#                      status_code=status.HTTP_200_OK)
# def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1), session: Session = Depends(get_session)) -> dict:
#     user = session.get(User, id)
#     if user is not None:
#         session.delete(user)
#         session.commit()
#         return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
#     else:
#         return JSONResponse(content={'message':f'Error. User id:{id} Not found'}, status_code=status.HTTP_404_NOT_FOUND)
