from fastmcp import FastMCP
from pydantic import BaseModel
from app.csv_db import add_user, list_users

mcp = FastMCP(name="User Registration server")

class Registration(BaseModel):
    name: str
    email: str
    dob: str

@mcp.tool()
def register_user(name: str, email: str, dob: str ) -> str:
    """Register a new user """
    add_user(name, email, dob)
    return f"User {name} registered successfully."

@mcp.tool()
def get_registrations():
    users = list_users()
    return {"users": users}

# Enable MCP-compatible tool exposure at /mcp

if __name__=="__main__":
    mcp.run(transport="streamable-http")