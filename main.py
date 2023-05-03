from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

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
    for user in users:
        if user['id']==id:
            return user
    return []

@app.get('/users/', tags=['users'])
def get_user_by_city(city:str):
    return []