from fastapi import APIRouter,Depends
from schemas.ai_authentication_schema import RegisterResponse, RegisterRequest, LogInRequest,LogInResponse
from services import authentication_services 
from dependencies.authentication_header import get_current_user_id


authentication_router = APIRouter(prefix="/authentication",)

@authentication_router.post("/sign_up/", response_model= RegisterResponse)
def authentication_sign_up(data : RegisterRequest):
    return authentication_services.store_users(data)

@authentication_router.post("/log_in/", response_model= LogInResponse)
def authentication_sign_up(data : LogInRequest):
    return authentication_services.verify_login(data)

@authentication_router.get("/me/")
def get_into_trip(user_id : int =Depends(get_current_user_id)):
    return {
        "user_id" : str(user_id),
        "message" : f"you're allowed to create or explore your trips"
    }



