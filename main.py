from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

class User(BaseModel):
    id: Optional[int] = None 
    name : str = Field(min_length=5, max_length=50)
    mail : str = Field(min_length=5, max_length=50)
    city : str = Field(min_length=5, max_length=50)
    initDate : Optional[str] = None 
    class Config:
        schema_extra = {
            'example': {
                'id' : 1,
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

@app.get('/users', tags=['users'])
def get_users():
    return users

@app.get('/user/{id}', tags=['users'])
def get_user(id: int):
    return [user for user in users if user['id'] == id]

@app.get('/users/', tags=['users'])
def get_user_by_city(city:str):
    return [user for user in users if user['city'] == city]

@app.post('/user', tags=['users'])
def create_user(user:User):
    users.append(user)
    return ['User added']

@app.put('/user/{id}', tags=['users'])
def update_user(id:int, user:User):
    userFiltered = [user for user in users if user['id'] == id]
    if len(userFiltered) == 1:
        userFiltered[0]['name']=user.name
        userFiltered[0]['mail']=user.mail
        userFiltered[0]['city']=user.city
        userFiltered[0]['initDate']=user.initDate
        return [{'message':f'User id:{id} updated correctly'}]
    else:
        return [{'message':f'Error id:{id} not Found'}]

@app.delete('/user/{id}',tags=['users'])
def delete_user(id:int):
    for user in users:
        if user['id']==id:
            users.remove(user)
            return [{'message':f'User id:{id} deleted'}]
    return [{'message':f'Error. User id:{id} Not found'}]
    # users = [user for user in users if user['id'] != id]    #Es una manera diferente de Eliminar de una lista el diccionario