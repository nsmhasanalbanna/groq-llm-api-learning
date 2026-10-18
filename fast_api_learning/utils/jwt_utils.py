from config.settings import settings
import jwt
from datetime import datetime,timedelta,timezone

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm

def create_access_token(user_id : int):
    if not JWT_SECRET_KEY:
        raise RuntimeError ("JWT_SECRET_KEY is not configured")

    now = datetime.now(timezone.utc)
    payload = {
        "sub" : str(user_id),
        "iat" : now,
        "exp" : now + timedelta(minutes=30)
    }

    return jwt.encode(payload,
                    JWT_SECRET_KEY,
                    algorithm=JWT_ALGORITHM
                    )

def decode_access_token(token:str):
    if not JWT_SECRET_KEY:
        raise RuntimeError ("JWT_SECRET_KEY is not configured")

    return jwt.decode(token,JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])
