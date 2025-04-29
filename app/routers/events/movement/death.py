from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/death",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)