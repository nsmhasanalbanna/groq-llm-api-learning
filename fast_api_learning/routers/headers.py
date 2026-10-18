from fastapi import FastAPI,APIRouter, Header

header = APIRouter(prefix="/header")

@header.get("/test/")
def test_header(x_api_key : str = Header()):
    return {
        "api_key" : x_api_key
    }

@header.get("/client/")
def test_header(x_client_version : str | None = Header(default=None)):
    return {
        "x_client_version" : x_client_version
    }

@header.get("/request/")
def test_alias(request_id : str  = Header(alias="X-Request-ID")):
    return {
        "request_id" : request_id
    }