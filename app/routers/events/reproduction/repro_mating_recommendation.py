"""
Collects API calls related to animal repro mating recommendation events.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.5.0 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.5.0/resources/icarReproMatingRecommendationResource.json
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
from ...icar.icarResources import (
    icarReproMatingRecommendationResource as ReproMatingRecommendation,
)
from ...users import User, get_current_active_user

ERROR_MSG_OBJECT = "Repro Mating Recommendation"

router = APIRouter(
    prefix="/repro_mating_recommendation",
    tags=["reproduction"],
    responses={404: {"description": "Not found"}},
)


class ReproMatingRecommendationCollection(BaseModel):
    repro_mating_recommendation: List[ReproMatingRecommendation]


@router.post(
    "/",
    response_description="Add repro mating recommendation event",
    response_model=ReproMatingRecommendation,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_repro_mating_recommendation_event(
    request: Request,
    repro_mating_recommendation: ReproMatingRecommendation,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_reproduction"])
    ],
):
    """
    Create a new repro mating recommendation event.

    :param repro_mating_recommendation: Mating recommendation to be added
    """
    return await add_one_to_db(
        repro_mating_recommendation,
        request.app.state.repro_mating_recommendation,
        ERROR_MSG_OBJECT,
    )


@router.delete("/{ft}", response_description="Delete event")
async def remove_repro_mating_recommendation_event(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_reproduction"])
    ],
    ft: mongo_object_id.MongoObjectId,
):
    """
    Delete a repro mating recommendation event.

    :param ft: ObjectID of the mating recommendation to be deleted
    """
    return await delete_one_from_db(
        request.app.state.repro_mating_recommendation, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for repro mating recommendation event",
    response_model=ReproMatingRecommendationCollection,
    response_model_by_alias=False,
)
async def repro_mating_recommendation_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_reproduction"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a repro mating recommendation event given the provided
    criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(
        request.app.state.repro_mating_recommendation, query
    )
    return ReproMatingRecommendationCollection(
        repro_mating_recommendation=result
    )
