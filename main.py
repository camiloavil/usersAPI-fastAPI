# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# APP
from app.routers.usersRouter import users_router
from app.routers.adminuserRouter import adminuser_router
from app.security.secureuser import secure_user
from app.DB.db import create_db_table

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(users_router)
app.include_router(adminuser_router)
app.include_router(secure_user)

@app.on_event('startup')
def on_startup():
    create_db_table()

@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

