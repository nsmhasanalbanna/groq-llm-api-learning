from fastapi import FastAPI,APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel,Field
from database.users_data import users
from schemas.user_schemas import*
from services import user_services
from services.exceptions import UserNotFoundError,BadRequestError


def get_app_name():
    return "AI Assistant"

def get_current_user():
    return {
        "name" : "Hasan",
        "role" : "admin"
    }

router = APIRouter(prefix="/users",
                dependencies=[Depends(get_current_user)]
)

def get_user_role(user = Depends(get_current_user)):
    return user["role"]


@router.get("/test/")
def test(app_name = Depends(get_app_name)):
    return {"message" : "users router working",
            "app_name" : app_name}


@router.post("/", status_code=201, response_model=UserResponseModel)
def create_user (data : Create_Users):
    return user_services.create_user(data)
   



@router.get("/{user_id}", response_model= UserResponse) #response_model is a built in FastAPI parameter which tells the fucntion to use the format
def send_user(user_id:int):
    return user_services.send_user(user_id)

@router.get("/", response_model=ListofUserResponse)
def get_users(limit:int = Query(10, ge = 1, le = 100), offset:int = Query(0, ge = 0,le = 100 ), min_age:int | None = Query(default=None,ge=1)):
    return user_services.get_users(limit,offset,min_age)

@router.delete("/{user_id}",status_code=204)
def del_user(user_id: int, confirm : bool = Query(default=False)):
    return user_services.del_user(user_id,confirm)
        



@router.put("/{user_id}",status_code=200)
def update_user(user_id:int, update : UserUpdate):
    return user_services.update_user(user_id, update)



@router.patch("/{user_id}")
def update_patch(user_id:int, patch:UpdatePatch):
     
    return user_services.update_patch(user_id, patch)

