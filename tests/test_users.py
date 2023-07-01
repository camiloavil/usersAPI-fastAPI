# pytest
import pytest
# FastAPI
from fastapi import status
from fastapi.testclient import TestClient
# APP
from app.models.user import SQLModel,User, UserBase, UserFB
from app.security.secureuser import get_password_hash
from app.DB.db import get_session
from app.DB.querys import add_user_to_db
# SQLModel
from sqlmodel import Session, create_engine
# Python
import os
import json

from main import app

#Filename of sqlite DB
TEST_SQLITE_FILENAME = 'test_DB.sqlite'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR,TEST_SQLITE_FILENAME)}' 
test_engine = create_engine(DATABASE_URL, echo = False)
SQLModel.metadata.create_all(test_engine)

def delete_db_file():
    os.remove(os.path.join(BASE_DIR, TEST_SQLITE_FILENAME))

def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(scope="function")
def client() -> TestClient:
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    return TestClient(app)

@pytest.fixture()
def setUp_users(client: TestClient):
    user1 = {
        "name": "Test user One",
        "email": "one@example.com",
        "password": "MyPassword",
        "city": "TestyCity",
        "country": "Testland",
        "userType": "admin"
        }
    user2 = {
        "name": "Test user Two",
        "email": "two@example.com",
        "password": "MyPassword",
        "city": "TestyCity",
        "country": "Testland",
        "userType": "test"
        }
    user3 = {
        "name": "Test user Tree",
        "email": "tree@example.com",
        "password": "MyPassword",
        "city": "TreeCity",
        "country": "Treeland",
        "userType": "test"
        }
    with Session(test_engine) as session:
        add_user_to_db(User(**user1, pass_hash= get_password_hash(user2["password"])),
                       session)
        add_user_to_db(User(**user2, pass_hash= get_password_hash(user2["password"])),
                       session)
        add_user_to_db(User(**user3, pass_hash= get_password_hash(user3["password"])),
                       session)
    yield user1,user2,user3

def test_create_newuser_blank(client: TestClient):
    response = client.post("/users/newuser")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "New User whitout fields is not valid"

def test_create_newuser_all_fields(client: TestClient):
    userData = {
        "name": "Testing",
        "email": "test@example.com",
        "password": "MyPassword",
        "city": "TestyCity",
        "country": "Testland",
        "userType": "admin"
        }
    response = client.post("/users/newuser",json=userData,)
    userData.pop('password')  # remove password it never should be returned
    userData['userType'] = 'free'       #All created users must be userType 'free'
    assert response.status_code == status.HTTP_201_CREATED, "Status code not 201"
    assert all(key in response.json() for key in userData) , "Response Incomplete or Wrong keys"
    assert UserBase(**response.json()) == UserBase(**userData), "User created is different" 
    assert 'pass_hash' not in response.json() , "pass_hash Should never be in the response"
    #Not necesary, is reduntant
    # assert response.json()['userType'] == 'free', "new users userType always should be free"   
    #Not necesary, is reduntant
    # assert isinstance(response.json(), dict), "Response is not a dictionary"

def test_create_newuser_repeted(client: TestClient):
    user = {
        "name": "Testing",
        "email": "test@example.com",
        "password": "MyPassword"
        }
    client.post("/users/newuser",json=user,)
    response = client.post("/users/newuser",json=user,)
    assert response.status_code == status.HTTP_409_CONFLICT, "Status code not 409 Conflict"

def test_check_login_of_user_check_his_info(client: TestClient, setUp_users: setUp_users):
    user1,user2,user3 = setUp_users
    response = client.post("/userlogin",data= {"username": user1['email'], "password": user1['password']})
    assert response.status_code == status.HTTP_200_OK, "Status code not 200 on login"
    assert 'access_token' in response.json(), "Response must have an access_token"
    assert response.json()['token_type'] == 'bearer', "Response must be token_type 'bearer'"
    header_user = {"Authorization" : "Bearer " + response.json()['access_token']}

    response = client.get("/users/myuser", headers=header_user)
    assert response.status_code == status.HTTP_200_OK, "Status code not 200 on path GET /users/myuser"
    assert all(key in response.json() for key in list(UserFB.__annotations__)) , "Response must have all keys of UserFB"
    assert all(key in response.json() for key in list(UserBase.__annotations__)) , "Response must have all keys of UserFB"
    assert (all( (user1[key] == response.json()[key]) for key in list(UserBase.__annotations__))) , "UserFB returned is different"
    assert user1['name'] == response.json()['name'], "Response must be equal in all fields"
    assert 'initDate' in response.json(), "Response must have an initDate"

#Not necesary, is reduntant
# def test_create_newuser_(client: TestClient):
#     params = {
#         "name": "Testing",
#         "email": "test@example.com",
#         "password": "MyPassword"
#         }
#     response = client.post("/users/newuser",json=params,)
#     params.pop('password')  # remove password it never should be returned
#     params['userType'] = 'free'
#     assert response.status_code == status.HTTP_201_CREATED, "Status code not 201"
#     assert all(key in response.json() for key in params) , "Response Incomplete. it hasn't all keys"
#     assert UserBase(**response.json()) == UserBase(**params), "User created is different" 
#     assert 'pass_hash' not in response.json() , "pass_hash Should never be in the response"


#     def test_info_user_path_without_credentials(self):
#         # response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
#         response = client.get("/users/myuser")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Status code not 401 on path GET /users/myuser"

#         response = client.put("/users/myuser")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Status code not 401 on path PUT /users/myuser"

#         response = client.delete("/users/myuser")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Status code not 401 on path DELETE /users/myuser"

#         response = client.put("/users/myuser/changepassword")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Status code not 401 on path PUT /users/myuser/changepassword"

#     def test_login_user_must_be_same_user(self):
#         # response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
#         setnew_dbTesting()
#         #create users
#         user1 = {"name": "Uno Name", "email": "uno@example.com", "password": "MyPassword1"}
#         user2 = {"name": "Dos Name", "email": "dos@example.com", "password": "MyPassword2"}
#         client.post("/users/newuser",json=user1,)
#         client.post("/users/newuser",json=user2,)
#         dataLoginError = {'username': 'value1', 'password': 'value2'}
#         response = client.post("/userlogin", data=dataLoginError)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Status code not 401 on path GET /users/myuser"

#         dataLogin1 = {'grant_type':'',
#                       'scope':'',
#                       'client_id':'',
#                       'client_secret':'',
#                       'username': user1["email"], 'password': user1["password"]}
        
#         dataLogin = {'username': user1["email"], 'password': user1["password"]}
#         print(str(dataLogin))
#         responseToken = client.post("/userlogin", 
#                                     headers={"Accept": "application/json",
#                                              "Content-Type": "application/x-www-form-urlencoded"}, 
#                                     data=dataLogin)
#                                     # json=dataLogin1)
#         print(str(responseToken.json()))
#         assert response.status_code == status.HTTP_200_OK, "Status code must be 200"
#         assert 'access_token' in responseToken.json(), "access_token must be in Correct Response"
#         # tokeUser1 = responseToken.json()['access_token']

        