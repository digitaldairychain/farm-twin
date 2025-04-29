from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/birth",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)