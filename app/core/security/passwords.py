from passlib.context import CryptContext
# from dotenv import load_dotenv
import os

# load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN = ""
# os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = ""
# os.getenv("REFRESH_TOKEN")
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
