from pydantic import BaseModel, Field, EmailStr

class RegisterRequest(BaseModel):
    email : EmailStr 
    password : str =Field(min_length=8)

class RegisterResponse(BaseModel):
    user_id : int
    email : EmailStr

class LogInRequest(BaseModel):
    email : EmailStr
    password : str

class LogInResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"




