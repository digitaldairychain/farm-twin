from fastapi import APIRouter

router = APIRouter(
    prefix="/carcass",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)