from fastmcp import FastMCP
from pydantic import BaseModel
from csv_db import add_user, list_users

mcp = FastMCP(name="User Registration server")


@mcp.tool()
def register_user(name: str, email: str, dob: str) -> dict:
    """Register a new user"""
    add_user(name, email, dob)
    return {"status": "success", "message": f"User {name} registered successfully."}


@mcp.tool()
def get_registrations() -> dict:
    """Get all registered users"""
    users = list_users()
    return {"users": users}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
