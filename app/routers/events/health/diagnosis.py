"""
Collects API calls related to an animal receiving a diagnosis.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.5.0 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.5.0/resources/icarDiagnosisEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
)
from ...icar.icarResources import icarDiagnosisEventResource as Diagnosis
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Diagnosis"

router = APIRouter(
    prefix="/diagnosis",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


class DiagnosisCollection(BaseModel):
    diagnosis: List[Diagnosis]


@router.post(
    "/",
    response_description="Add diagnosis event",
    response_model=Diagnosis,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_diagnosis_event(
    request: Request,
    diagnosis: Diagnosis,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_health"])
    ]
):
    """
    Create a new diagnosis event.

    :param diagnosis: Diagnosis to be added
    """
    return await add_one_to_db(
        diagnosis, request.app.state.diagnosis, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a diagnosis event")
async def remove_diagnosis_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_health"])
    ],
):
    """
    Delete a diagnosis event.

    :param ft: ObjectID of the diagnosis event to delete
    """
    return await delete_one_from_db(
        request.app.state.diagnosis, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for diagnosis event",
    response_model=DiagnosisCollection,
    response_model_by_alias=False,
)
async def diagnosis_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_health"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a diagnosis event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.diagnosis, query)
    return DiagnosisCollection(diagnosis=result)
