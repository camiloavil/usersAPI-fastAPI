from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.routers.users_router import users_router
from app.config.db import create_db_table

import time

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(users_router)

@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        print(f"MAIN Error Handler Exception: {str(e)}")
        return JSONResponse(status_code=500, content={'error': str(e)})

@app.on_event('startup')
def on_startup():
    create_db_table()

@app.get('/', tags=['home'])
def home():
    return HTMLResponse('<h1>Hello You</h1>')

