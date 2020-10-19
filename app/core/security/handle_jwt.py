import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Request

from datetime import datetime, timedelta

from .passwords import ALGORITHM, ACCESS_TOKEN, REFRESH_TOKEN

ACCESS_TOKEN_EXPIRE_MINUTES = 43200

class OAuth2PasswordCookie(OAuth2PasswordBearer):
    """OAuth2 password flow with token in a httpOnly cookie.
    """

    def __init__(self, *args, token_name: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._token_name = token_name or "jid"

    @property
    def token_name(self) -> str:
        """Get the name of the token's cookie.
        """
        return self._token_name

    async def __call__(self, request: Request) -> str:
        """Extract and return a JWT from the request cookies.
        Raises:
            HTTPException: 403 error if no token cookie is present.
        """
        token = request.cookies.get(self._token_name)
        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return token


oauth2_scheme = OAuth2PasswordCookie(tokenUrl="/api/token")


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(*, data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt
