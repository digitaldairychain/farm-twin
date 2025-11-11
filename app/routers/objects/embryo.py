"""
Collects API calls related to embryos.

This collection of endpoints allows for the addition, deletion
and finding of embryos.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
    update_one_in_db,
)
from ..icar.icarResources import icarReproEmbryoResource as Embryo
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/embryo",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Embryo"


class EmbryoCollection(BaseModel):
    embryo: List[Embryo]


@router.post(
    "/",
    response_description="Add new embryo",
    response_model=Embryo,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_embryo(
    request: Request,
    embryo: Embryo,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_embryo"])
    ],
):
    """
    Create a new embryo.

    :param embryo: Embryo to be added
    """
    return await add_one_to_db(embryo, request.app.state.embryo, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete an embryo")
async def remove_embryo(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_embryo"])
    ],
):
    """
    Delete a embryo.

    :param ft: UUID of the embryo to delete
    """
    return await delete_one_from_db(request.app.state.embryo, ft, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update an embryo",
    response_model=Embryo,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_embryo(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    embryo: Embryo,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_embryo"])
    ],
):
    """
    Update an existing embryo if it exists.

    :param ft: UUID of the embryo to update
    :param embryo: Embryo to update with
    """
    return await update_one_in_db(
        embryo, request.app.state.embryo, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for an embryo",
    response_model=EmbryoCollection,
    response_model_by_alias=False,
)
async def embryo_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_embryo"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    id: str | None = None,
    name: str | None = None,
    collectionCentre: str | None = None,
    dateCollected: datetime | None = None,
    donorURI: str | None = None,
    sireOfficialName: str | None = None,
    sireURI: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a embryo given the provided criteria."""
    query = {
        "_id": ft,
        "id": id,
        "name": name,
        "collectionCentre": collectionCentre,
        "dateCollected": dateCollected,
        "donorURI": donorURI,
        "sireOfficialName": sireOfficialName,
        "sireURI": sireURI,
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.embryo, query)
    return EmbryoCollection(embryo=result)
