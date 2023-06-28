# FastAPI
from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
# APP
from app.routers import filesRouter, usersRouter, adminRouter
from app.security import secureuser
from app.DB.db import create_db_table
# Python
import time

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

app.include_router(usersRouter.router, 
                   prefix='/users',
                   tags=['Users'])
app.include_router(adminRouter.router,
                   prefix='/admin',
                   tags=['Admin'])
app.include_router(secureuser.router)
app.include_router(filesRouter.router)   

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

@app.get(path='/', 
         tags=['home'],
         status_code=status.HTTP_200_OK)
def home():
    return HTMLResponse('<h1>Hello You</h1>')

