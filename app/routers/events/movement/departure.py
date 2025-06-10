from fastapi import APIRouter

router = APIRouter(
    prefix="/departure",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)