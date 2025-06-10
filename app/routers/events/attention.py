from fastapi import APIRouter

router = APIRouter(
    prefix="/attention",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)