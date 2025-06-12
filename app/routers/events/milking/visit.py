from fastapi import APIRouter

router = APIRouter(
    prefix="/visit",
    tags=["events", "milking"],
    responses={404: {"description": "Not found"}},
)
