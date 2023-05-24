from fastapi import APIRouter, Depends, Path, status, Body, Query
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime

from app.models.user import User, UserCreate, UserUpdate
from app.models.response import ResponseModel
from app.config.db import get_session
from sqlmodel import Session, select

users_router = APIRouter()

@users_router.get('/users', tags=['users'], response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(session: Session = Depends(get_session)) -> List[User]:
    users = session.exec(select(User)).all()
    return users

@users_router.get('/user/{id}', tags=['users'], response_model=User, status_code=status.HTTP_200_OK)
def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1), session: Session = Depends(get_session)) -> User:
    user = session.get(User, id)
    if user is not None:
        return user
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= {'message' : f'Error. User id:{id} Not found'})

@users_router.delete('/user/{id}', tags=['users'], response_model=ResponseModel, status_code=status.HTTP_200_OK)
def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1), session: Session = Depends(get_session)) -> dict:
    user = session.get(User, id)
    if user is not None:
        session.delete(user)
        session.commit()
        return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message':f'Error. User id:{id} Not found'}, status_code=status.HTTP_404_NOT_FOUND)

@users_router.get('/users/', tags=['users'],response_model=List[User],status_code=status.HTTP_200_OK)
def get_user_by_city(city:str = Query(description='look for City',example='Neiva', min_length=2,max_length=20)) -> List[User]:
    data = [user for user in users if user['city'] == city]
    if len(data)==0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=data) #Not Found
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,content=data) #Not Found

@users_router.post('/user', tags=['users'],response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate = Body(...), session: Session = Depends(get_session)) -> dict:
    user_db = User.from_orm(user)
    user_db.initDate = datetime.now()
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message' : 'User added', 'id' : user_db.id, 'username' : user_db.name })

@users_router.put('/user/{id}', tags=['users'],response_model=ResponseModel, status_code=status.HTTP_200_OK)
def update_user(id:int = Path(description="User ID to modify",example=1,ge=1), user:UserUpdate = Body(), session: Session = Depends(get_session)) -> dict:
    user_db = session.get(User,id)
    if user_db is None:
        return JSONResponse(content={'message':f'Error id:{id} not Found'},status_code=status.HTTP_404_NOT_FOUND)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db,key,value)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return JSONResponse(content={'message':f'User id:{id} updated correctly'},status_code=status.HTTP_200_OK)
