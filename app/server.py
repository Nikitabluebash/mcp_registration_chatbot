from fastmcp import FastMCP
from pydantic import BaseModel
from csv_db import add_user, list_users

mcp = FastMCP(name="User Registration server")


mcp.tool(description="""Register a new user by saving their info to a CSV.""")(add_user)


mcp.tool(description="""
This tool fetches all previously stored user data from the CSV file and formats it for display.
""")(list_users)

if __name__ == "__main__":
    # Use "http" transport for simplicity and clearer debugging
    mcp.run(transport="http", host="0.0.0.0", port=8000)