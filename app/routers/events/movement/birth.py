from fastapi import APIRouter

router = APIRouter(
    prefix="/birth",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)