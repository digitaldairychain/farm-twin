"""
Collects API calls related to an animal receiving treatment.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.5.0 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.5.0/resources/icarTreatmentEventResource.json
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
from ...icar.icarResources import icarTreatmentEventResource as Treatment
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Treatment"

router = APIRouter(
    prefix="/treatment",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


class TreatmentCollection(BaseModel):
    treatment: List[Treatment]


@router.post(
    "/",
    response_description="Add treatment event",
    response_model=Treatment,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_treatment_event(
    request: Request,
    treatment: Treatment,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_health"])
    ]
):
    """
    Create a new treatment event.

    :param treatment: Treatment to be added
    """
    return await add_one_to_db(
        treatment, request.app.state.treatment, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a treatment event")
async def remove_treatment_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_health"])
    ],
):
    """
    Delete a treatment event.

    :param ft: ObjectID of the treatment event to delete
    """
    return await delete_one_from_db(
        request.app.state.treatment, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for treatment event",
    response_model=TreatmentCollection,
    response_model_by_alias=False,
)
async def treatment_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_health"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    procedure: str | None = None,
    site: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a treatment event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "procedure": procedure,
        "site": site,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.treatment, query)
    return TreatmentCollection(treatment=result)
