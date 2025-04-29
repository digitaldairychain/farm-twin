from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/health",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)