from fastapi import FastAPI

app = FastAPI()
app.title = "Users API"
app.version = "0.0.1"

@app.get('/', tags=['home'])
def home():
    return "Hello you"