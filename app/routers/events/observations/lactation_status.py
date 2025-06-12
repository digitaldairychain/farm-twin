from fastapi import APIRouter

router = APIRouter(
    prefix="/lactation_status",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)
