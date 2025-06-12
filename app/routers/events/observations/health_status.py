from fastapi import APIRouter

router = APIRouter(
    prefix="/health_status",
    tags=["events", "observations"],
    responses={404: {"description": "Not found"}},
)
