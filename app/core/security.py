import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi import HTTPException, Request


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
        print(token)
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# PASSWORD RELATED
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "super_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
