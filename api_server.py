from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database 

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

class DroneCreate(BaseModel): 
    name: str
    description: str

class DeleteRequest(BaseModel):
    name: str

class UpdateRequest(BaseModel):
    old_name: str
    new_name: str
    description: str


@app.post("/login")
def login_api(data: LoginRequest):
    user_exists = database.check_user(data.email, data.password)
    if user_exists:
        role = "admin" if data.email == "admin@mail.com" else "user"
        return {"status": "success", "role": role}
    raise HTTPException(status_code=401, detail="Xətalı giriş!")

@app.post("/signup")
def signup_api(data: SignupRequest):
    success = database.register_user(data.email, data.password)
    if success:
        return {"status": "created"}
    raise HTTPException(status_code=400, detail="İstifadəçi artıq mövcuddur!")

@app.get("/drones")
def get_drones_api():
    return database.get_drones()

@app.post("/add_drone")
def add_drone_api(drone: DroneCreate):
    database.add_drone(drone.name, drone.description)
    return {"status": "success"}

@app.post("/delete_drone")
def delete_drone_api(data: DeleteRequest):
    database.delete_drone(data.name)
    return {"status": "deleted"}

@app.post("/update_drone")
def update_drone_api(data: UpdateRequest):
    database.update_drone(data.old_name, data.new_name, data.description)
    return {"status": "updated"}