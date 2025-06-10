from fastapi import APIRouter

router = APIRouter(
    prefix="/arrival",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)