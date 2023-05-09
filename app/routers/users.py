from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from . import users

users_router = APIRouter()


@users_router.delete('/user/{id}',tags=['users'],response_model=dict,status_code=status.HTTP_200_OK)
def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1)) -> dict:
    for user in users:
        if user['id']==id:
            users.remove(user)
            return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
    return JSONResponse(content={'message':f'Error. User id:{id} Not found'},status_code=status.HTTP_404_NOT_FOUND)
    # users = [user for user in users if user['id'] != id]    #Es una manera diferente de Eliminar de una lista el diccionario