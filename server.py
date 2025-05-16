from mcp.server.fastmcp import FastMCP
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdobeMCP")

# Create an MCP server
mcp = FastMCP("Adobe MCP")

# Ejemplo de leer un parametro de entorno
# user_email = os.getenv("USER_EMAIL")
# if not user_email:
#     logger.error("USER_EMAIL environment variable is not set.")
#     raise ValueError("USER_EMAIL environment variable is not set.")

if __name__ == "__main__":
    mcp.run(transport="stdio")  