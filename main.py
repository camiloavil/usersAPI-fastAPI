from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.routers.users import users_router

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(users_router)

class UserAuth(BaseModel):
    email    : str = Field(min_length=5, max_length=50)
    password : str = Field(min_length=5, max_length=50)


@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

