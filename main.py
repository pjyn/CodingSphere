from fastapi import FastAPI, HTTPException, Depends, Request
from mongoengine import connect
from app.models import User
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.crud import create_project, get_projects
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"

app = FastAPI()

# Connect to MongoDB
connect(host="mongodb://localhost:27017/jwt_auth_db")

@app.post("/register")
async def register(request: RegisterRequest):
    body = await request.body()
    print(f"Raw request body: {body.decode('utf-8')}")
    print(f"Received request: {request}")
    if User.objects(username=request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(request.password)
    user = User(username=request.username, password=hashed_password, role=request.role)
    user.save()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):
    user = User.objects(username=username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")@app.post("/register")
    


@app.get("/projects")
def list_projects():
    return get_projects()

@app.post("/projects")
def add_project(name: str, description: str, user=Depends(get_current_user)):
    return create_project(name, description, user)
