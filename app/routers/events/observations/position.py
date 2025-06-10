from fastapi import APIRouter

router = APIRouter(
    prefix="/position",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)