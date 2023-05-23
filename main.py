from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers.users_router import users_router
from app.config.db import create_db_table

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(users_router)

@app.on_event('startup')
def on_startup():
    create_db_table()

@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

