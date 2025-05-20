import httpx
import logging
import time
import threading

import asyncio

max_retries = 1
access_tokens = None
TOKEN_DURATION = 30 * 60  # 30 minutos en segundos

def guardar_access_token(token):
    global access_tokens
    expiry_time = time.time() + TOKEN_DURATION
    access_tokens = {'token': token, 'expiry': expiry_time}
    threading.Timer(TOKEN_DURATION, eliminar_access_token).start()

def obtener_access_token():
    print(f"obtener_access_token {access_tokens}")
    if access_tokens and access_tokens['expiry'] > time.time():
        return access_tokens['token']
    return None

def eliminar_access_token():
    global access_tokens
    access_tokens = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdboeCalls")

async def generate_access_token(api_key, client_secret, scopes):
    url = f"https://ims-na1.adobelogin.com/ims/token/v2?grant_type=client_credentials&client_id={api_key}&client_secret={client_secret}&scope={scopes}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    async with httpx.AsyncClient(verify=False) as client:  # Deshabilitar verificación SSL
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            token = response_json["access_token"]
            guardar_access_token(token)
            return None
        except httpx.RequestError as e:
            logger.exception(f"Error al obtener el JWT y la URL base: {e}")
            return None
        
async def obtener_listado_actividades(api_key, client_secret, scopes, tenant_id, ims_org, retries=0):
    token = obtener_access_token()

    if not token:
        await generate_access_token(api_key, client_secret, scopes)
        token = obtener_access_token()

    logger.info(f"Token de acceso: {token}")
    url = f"https://mc.adobe.io/{tenant_id}/target/activities"
    headers = {"Authorization": f"Bearer {token}", "x-api-key": api_key, "x-gw-ims-org-id": ims_org}

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.exception("Error al obtener el listado de actividades: %s", e)
            if response.status_code == 401 and retries < max_retries:  # Unauthorized
                logger.info("Token expirado, obteniendo un nuevo token...")
                await asyncio.sleep(1)
                return await obtener_listado_actividades(api_key, client_secret, scopes, tenant_id, ims_org, retries + 1)
            return []