import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


class Settings:
    jwt_secret_key: str = os.environ["JWT_SECRET_KEY"]
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_days: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_DAYS", "2")
    )


settings = Settings()
