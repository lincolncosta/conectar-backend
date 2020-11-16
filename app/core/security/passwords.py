from passlib.context import CryptContext
from dotenv import load_dotenv
import os, random, string

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
ALGORITHM = os.getenv("ALGORITHM")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_random_string(length: int = 64):
    letters = string.ascii_letters
    result = ''.join(random.choice(letters) for i in range(length))
    return result