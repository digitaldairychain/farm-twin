from fastapi import status, HTTPException, Response, APIRouter, Request


router = APIRouter(
    prefix="/lactation_status",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)