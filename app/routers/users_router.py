from fastapi import APIRouter, Path, status, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional ,List
from datetime import datetime

# from app.models.user import User
from app.config.db import engine

from . import users
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = None 
    name  : str = Field(min_length=3, max_length=50)
    email : str = Field(min_length=10, max_length=50)
    city  : str = Field(min_length=3, max_length=50)
    initDate : Optional[datetime] = None
    class Config:
        schema_extra = {
            'example': {
                'name' : 'Nombre',
                'email' : 'Correo Electronico, sera el validador de usuario',
                'city' : 'Ciudad'
            }
        }

users_router = APIRouter()

@users_router.get('/users', tags=['users'], response_model=List[User], status_code=status.HTTP_200_OK)
def get_users() -> List[User]:
    print(users)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@users_router.get('/user/{id}', tags=['users'], response_model=User, status_code=status.HTTP_200_OK)
def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1)) -> User:
    data = [user for user in users if user['id'] == id]
    if len(data)==1:
        return JSONResponse(status_code=status.HTTP_200_OK,content= data)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= data)

@users_router.delete('/user/{id}',tags=['users'],response_model=dict,status_code=status.HTTP_200_OK)
def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1)) -> dict:
    for user in users:
        if user['id']==id:
            users.remove(user)
            return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
    return JSONResponse(content={'message':f'Error. User id:{id} Not found'},status_code=status.HTTP_404_NOT_FOUND)
    # users = [user for user in users if user['id'] != id]    #Es una manera diferente de Eliminar de una lista el diccionario


@users_router.get('/users/', tags=['users'],response_model=List[User],status_code=status.HTTP_200_OK)
def get_user_by_city(city:str = Query(description='look for City',example='Neiva', min_length=2,max_length=20)) -> List[User]:
    data = [user for user in users if user['city'] == city]
    if len(data)==0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=data) #Not Found
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,content=data) #Not Found

@users_router.post('/user', tags=['users'],response_model=dict,status_code=status.HTTP_201_CREATED)
def create_user(user:User = Body(...)) -> dict:
    user = dict(user)                                           #make it a dict to add 'id' and 'initDate'
    user['id']=max(users, key=lambda x: x['id'])['id'] + 1
    user['initDate'] = datetime.now().strftime("%d/%m/%Y")
    users.append(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message' : 'User added'})

@users_router.put('/user/{id}', tags=['users'],response_model=dict, status_code=status.HTTP_200_OK)
def update_user(id:int = Path(description="User ID to modify",example=1,ge=1), user:User = Body()) -> dict:
    userFiltered = [user for user in users if user['id'] == id]
    if len(userFiltered) == 1:
        userFiltered[0]['name']=user.name
        userFiltered[0]['email']=user.email
        userFiltered[0]['city']=user.city
        userFiltered[0]['initDate']=user.initDate
        return JSONResponse(content={'message':f'User id:{id} updated correctly'},status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message':f'Error id:{id} not Found'},status_code=status.HTTP_404_NOT_FOUND)

