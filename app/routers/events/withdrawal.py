from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/withdrawal",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)
