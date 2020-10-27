import os
from dotenv import load_dotenv

from pathlib import Path

env = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env)

PROJECT_NAME = "conectar"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
API_V1_STR = "/api/v1"
