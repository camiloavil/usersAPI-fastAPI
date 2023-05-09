from fastapi import FastAPI, Body, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

# class JWTBearer(HTTPBearer):
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)
#         data = validate_token(auth.credentials)
#         if data['email']!='admin@admin.com':
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are invalid')

class UserAuth(BaseModel):
    email    : str = Field(min_length=5, max_length=50)
    password : str = Field(min_length=5, max_length=50)

class User(BaseModel):
    id: Optional[int] = None 
    name  : str = Field(min_length=10, max_length=50)
    email : str = Field(min_length=10, max_length=50)
    city  : str = Field(min_length=10, max_length=50)
    initDate : Optional[datetime] = None
    class Config:
        schema_extra = {
            'example': {
                'id' : 'Identifier',
                'name' : 'Nombre',
                'mail' : 'Correo Electronico, sera el validador de usuario',
                'city' : 'Ciudad',
                'initDate' : 'Fecha de inscripccion'
            }
        }

users = [
    {
        'id'   : 1,
        'name' : 'Camilo Avila',
        'mail' : 'camilo.avil@gmail.com',
        'city' : 'Neiva',
        'initDate' : '2May2023'
    },
    { 
        'id'   : 2,  
        'name' : 'Martin Castro',
        'mail' : 'castro.martin@gmail.com',
        'city' : 'Pasto',
        'initDate' : '20Ener2023'
    }
]

@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

@app.get('/users', tags=['users'], response_model=List[User], status_code=status.HTTP_200_OK)
def get_users() -> List[User]:
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@app.get('/user/{id}', tags=['users'], response_model=User, status_code=status.HTTP_200_OK)
def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1)) -> User:
    data = [user for user in users if user['id'] == id]
    if len(data)==1:
        return JSONResponse(status_code=status.HTTP_200_OK,content= data)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= data)

@app.get('/users/', tags=['users'],response_model=List[User],status_code=status.HTTP_200_OK)
def get_user_by_city(city:str = Query(description='look for City',example='Neiva', min_length=2,max_length=20)) -> List[User]:
    data = [user for user in users if user['city'] == city]
    if len(data)==0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=data) #Not Found
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,content=data) #Not Found

@app.post('/user', tags=['users'],response_model=dict,status_code=status.HTTP_201_CREATED)
def create_user(user:User = Body()) -> dict:
    users.append(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'message' : 'User added'})

@app.put('/user/{id}', tags=['users'],response_model=dict, status_code=status.HTTP_200_OK)
def update_user(id:int = Path(description="User ID to modify",example=1,ge=1), user:User = Body()) -> dict:
    userFiltered = [user for user in users if user['id'] == id]
    if len(userFiltered) == 1:
        userFiltered[0]['name']=user.name
        userFiltered[0]['mail']=user.mail
        userFiltered[0]['city']=user.city
        userFiltered[0]['initDate']=user.initDate
        return JSONResponse(content={'message':f'User id:{id} updated correctly'},status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message':f'Error id:{id} not Found'},status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/user/{id}',tags=['users'],response_model=dict,status_code=status.HTTP_200_OK)
def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1)) -> dict:
    for user in users:
        if user['id']==id:
            users.remove(user)
            return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
    return JSONResponse(content={'message':f'Error. User id:{id} Not found'},status_code=status.HTTP_404_NOT_FOUND)
    # users = [user for user in users if user['id'] != id]    #Es una manera diferente de Eliminar de una lista el diccionario