from fastapi import FastAPI,Query,Header,Cookie,Response
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from fastapi import HTTPException
from routers.users import router
from routers.ai import ai_router
from routers.headers import header
from routers.authentication import authentication_router
from services.exceptions import UserNotFoundError, BadRequestError




app = FastAPI()

app.include_router(router)
app.include_router(ai_router)
app.include_router(header)
app.include_router(authentication_router)

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request : Request, exec : UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content= {"detail":"user not found"}
    )
@app.exception_handler(BadRequestError)
async def bad_request_handler(request : Request, exec : BadRequestError):
    return JSONResponse(
        status_code=400,
        content= {"detail":"bad request"}
    )


@app.get("/cookie-test/")
def test_cookie(session_id : str | None = Cookie(default=None)):
    return {
            "session_id" : session_id
        }

@app.get("/set-cookie/")
def set_cookie(response : Response):
    response.set_cookie(
        key= "session_id",
        value= "password"
    )
    return {
        "message" : "cookie set"
    }
