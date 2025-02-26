from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

API_KEY = os.getenv("API_KEY")

async def api_key_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Authentication function to verify API Key.

    Args:
        credentials (HTTPAuthorizationCredentials): The provided API key.

    Raises:
        HTTPException: If the API key is invalid or missing.

    Returns:
        str: The valid API key if authentication is successful.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key is not set in the environment variables.")

    if not credentials or credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    return credentials.credentials
