from fastapi import APIRouter

router = APIRouter(
    prefix="/repro_status",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)