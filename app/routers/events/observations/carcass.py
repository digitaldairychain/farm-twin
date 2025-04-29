from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/carcass",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)