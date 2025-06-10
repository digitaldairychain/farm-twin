from fastapi import APIRouter

router = APIRouter(
    prefix="/death",
    tags=["events", "movement"],
    responses={404: {"description": "Not found"}},
)