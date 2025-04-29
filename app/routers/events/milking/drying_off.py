from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/drying_off",
    tags=["events", "milking"],
    responses={404: {"description": "Not found"}},
)