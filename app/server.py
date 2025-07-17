from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from app.csv_db import add_user, list_users

app = FastAPI()
mcp = FastApiMCP(app, name="Local CSV Registration Bot")

class Registration(BaseModel):
    name: str
    email: str
    dob: str

@app.post("/register", operation_id="register_user", summary="Register a user")
def register_user(data: Registration):
    add_user(data.name, data.email, data.dob)
    return {"status":"success","message": f"✅ {data.name} registered successfully."}

@app.get("/registrations", operation_id="get_registrations", summary="Get all registrations")
def get_registrations():
    users = list_users()
    return {"users": users}

# Enable MCP-compatible tool exposure at /mcp
mcp.mount()
