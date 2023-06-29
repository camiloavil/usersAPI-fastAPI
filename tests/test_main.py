# FastAPI
from fastapi import status
from fastapi.testclient import TestClient
# APP
from app.models.user import SQLModel
from app.DB.db import get_session
# SQLModel
from sqlmodel import Session, create_engine
# Python
import os

from main import app

client = TestClient(app)


#Filename of sqlite DB
TEST_SQLITE_FILENAME = 'test_DB.sqlite'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR,TEST_SQLITE_FILENAME)}' 
test_engine = create_engine(DATABASE_URL, echo = False)
#Delete the previous DB File from the last one test 
os.remove(os.path.join(BASE_DIR, TEST_SQLITE_FILENAME))        
SQLModel.metadata.create_all(test_engine)

def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@app.on_event("shutdown")
async def shutdown_event():
    os.remove(os.path.join(BASE_DIR, TEST_SQLITE_FILENAME))

def test_home_item():
    # response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

class TestUsers:
    def test_create_newuser_blank(self):
        response = client.post("/users/newuser")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': [{'loc': ['body'],
                                                'msg': 'field required',
                                                'type': 'value_error.missing'}]}

    def test_create_newuser(self):
        params = {
            "name": "Testing",
            "email": "test@example.com",
            "password": "MyPassword",
            "city": "TestyCity",
            "country": "Testland"
            }
        response = client.post("/users/newuser",json=params,)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {'detail': [{'loc': ['body'],
                                                'msg': 'field required',
                                                'type': 'value_error.missing'}]}

    def test_info_user_path_without_credentials(self):
        # response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
        response = client.get("/users/myuser")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # assert response.json() == {
        #     "id": "foo",
        #     "title": "Foo",
        #     "description": "There goes my hero",
        # }

