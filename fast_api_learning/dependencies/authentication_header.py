from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_utils import decode_access_token
import jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/authentication/log_in/"
)
def get_current_user_id(token : str =Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid or expired authentication token",
                                headers={"WWW-Authenticate": "Bearer"}
                                )
        return int(user_id)

    except (jwt.InvalidTokenError, ValueError): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid or expired authentication token",
                                headers={"WWW-Authenticate": "Bearer"}
                                )