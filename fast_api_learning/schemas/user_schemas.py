from pydantic import BaseModel,Field

class UserResponseModel(BaseModel):
    user_id : int
    name : str
    age : int

class Create_Users(BaseModel):
    name : str = Field(min_length = 2)
    age : int = Field(gt = 18)

class UserResponse(BaseModel):
    user_id : int
    name : str
    age : int

class AdminResponse(BaseModel):
    user_id : int
    name : str
    age : int
    role : str

class ListofUserResponse(BaseModel):
    items : list[UserResponse]
    limit : int
    offset : int
    total : int

class UserUpdate(BaseModel):
    name : str 
    age : int 

class UpdatePatch(BaseModel):
    name : str | None = Field(default=None, min_length=2)
    age : int | None = Field(default=None, gt=18)




