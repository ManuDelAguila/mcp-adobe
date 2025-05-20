from mcp.server.fastmcp import FastMCP
import logging
import os
from adobe import obtener_listado_actividades

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdobeMCP")

# Create an MCP server
mcp = FastMCP("Adobe MCP")


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logger.error("API_KEY environment variable is not set.")
    raise ValueError("API_KEY environment variable is not set.")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    logger.error("CLIENT_SECRET environment variable is not set.")
    raise ValueError("CLIENT_SECRET environment variable is not set.")

SCOPES = os.getenv("SCOPES")
if not SCOPES:
    logger.error("SCOPES environment variable is not set.")
    raise ValueError("SCOPES environment variable is not set.")

IMS_ORG = os.getenv("IMS_ORG")
if not IMS_ORG:
    logger.error("IMS_ORG environment variable is not set.")
    raise ValueError("IMS_ORG environment variable is not set.")

TENANT_ID = os.getenv("TENANT_ID")
if not TENANT_ID:
    logger.error("TENANT_ID environment variable is not set.")
    raise ValueError("TENANT_ID environment variable is not set.")


@mcp.tool()
async def obtener_listado_actividades_target() -> dict:
    """
    Obtiene el listado de actividades de Target.
    
    Returns:
        dict: El listado de actividades de Target.
    """
    try:
        actividades = await obtener_listado_actividades(
            api_key=API_KEY,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES,
            tenant_id=TENANT_ID,
            ims_org=IMS_ORG
        )
        return actividades
    except Exception as e:
        logger.error(f"Error al obtener el listado de actividades: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")  