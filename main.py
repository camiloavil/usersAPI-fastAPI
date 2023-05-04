from fastapi import FastAPI, Body
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
    return [user for user in users if user['id'] == id]

@app.get('/users/', tags=['users'])
def get_user_by_city(city:str):
    return [user for user in users if user['city'] == city]

@app.post('/user', tags=['users'])
def create_user(id:int=Body(),name:str=Body(),mail:str=Body(),city:str=Body(),initDate:str=Body()):
    users.append({
        'id'   : id,  
        'name' : name,
        'mail' : mail,
        'city' : city,
        'initDate' : initDate
    })
    return ['User added']

@app.put('/user/{id}', tags=['users'])
def update_user(id:int,name:str=Body(),mail:str=Body(),city:str=Body(),initDate:str=Body()):
    user = [user for user in users if user['id'] == id]
    if len(user) == 1:
        user[0]['name']=name
        user[0]['mail']=mail
        user[0]['city']=city
        user[0]['initDate']=initDate
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