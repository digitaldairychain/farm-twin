from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/conformation",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)