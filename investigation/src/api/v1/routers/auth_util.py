import httpx
from fastapi import Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.v1.schemas.schemas import AuthUser

oauth2_scheme = HTTPBearer()


async def get_current_user(
    auth_credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    try:
        async with httpx.AsyncClient() as client:
            url = 'http://nginx/api/v1/auth/verify_token'
            headers = {"Authorization": f'Bearer {auth_credentials.credentials}'}
            response = await client.get(url, headers=headers)
            auth_user_data = response.json()
            is_auth = AuthUser(**auth_user_data)
            logger.info("User authenticated successfully: %s", is_auth.username)
            return is_auth
    except httpx.HTTPError:
        logger.error("Could not validate credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
