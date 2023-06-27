
# @users_router.get('/users', tags=['users'], 
#                   response_model=List[User], 
#                   status_code=status.HTTP_200_OK
#                 )
# def get_users(offset: int = Query(description='Offset of the query',default=1,ge=1),
#               limit: int = Query(description='Limit of data per request',default=100, lte=100), 
#               session: Session = Depends(get_session)) -> List[User]:
#     users = session.exec(select(User).offset(offset).limit(limit)).all()
#     return users

# @users_router.get(path='/user/{id}', 
#                   tags=['users'], 
#                   response_model=User, 
#                   status_code=status.HTTP_200_OK)
# def get_user(id: int = Path(description='ID of the user to get',example=1,ge=1), 
#              session: Session = Depends(get_session)) -> User:
#     """
#     Retrieves a user by their ID. 
    
#     Args:
#         id (int): ID of the user to retrieve. Must be greater than or equal to 1.
#         session (Session): A SQLAlchemy Database Session dependency.

#     Returns:
#         User: A Pydantic User model representing the retrieved user.
#         JSONResponse (status_code=404): A JSON response containing an error message if the user is not found.
#     """
#     user = session.get(User, id)
#     if user is not None:
#         return user
#     else:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content= {'message' : f'Error. User id:{id} Not found'})



# # @users_router.delete(path='/user/{id}', 
# #                      tags=['AdminUsers'], 
# #                      response_model=ResponseModel, 
# #                      status_code=status.HTTP_200_OK)
# # def delete_user(id:int = Path(description="User ID to delete",example=1,ge=1), session: Session = Depends(get_session)) -> dict:
# #     user = session.get(User, id)
# #     if user is not None:
# #         session.delete(user)
# #         session.commit()
# #         return JSONResponse(content={'message':f'User id:{id} deleted'},status_code=status.HTTP_200_OK)
# #     else:
# #         return JSONResponse(content={'message':f'Error. User id:{id} Not found'}, status_code=status.HTTP_404_NOT_FOUND)
