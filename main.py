from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers.users_router import users_router
from app.DB.db import create_db_table
from app.security.secureuser import secure_user

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(users_router)
app.include_router(secure_user)

@app.on_event('startup')
def on_startup():
    create_db_table()

@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

