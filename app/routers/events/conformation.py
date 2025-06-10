"""
Collects API calls related to conformation events.

A conformation resource used to indicate that product should be separated
(e.g. colostrum from newly lactating cows).

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarConformationScoreEventResource.json
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request, Query
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing import List, Optional
from typing_extensions import Annotated
from datetime import datetime
from bson.objectid import ObjectId
from ..icar import icarEnums
from ..ftCommon import filterQuery
from .eventCommon import AnimalEventModel

router = APIRouter(
    prefix="/conformation",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


class Conformation(AnimalEventModel):
    traitGroup: Optional[icarEnums.icarConformationTraitGroupType] = Field(
        default=None,
        json_schema_extra={
            "description": "Defines whether the trait is a composite trait " +
            "or a linear trait.",
            "example": "Composite",
        },
    )
    score: int = Field(
        json_schema_extra={
            "description": "Conformation score with values of 1 to 9 " +
            "numeric in case of linear traits and for composites in most " +
            "cases between 50 and 99",
            "example": 47,
        },
    )
    traitScored: icarEnums.icarConformationTraitType = Field(
        json_schema_extra={
            "description": "Scored conformation trait type according " +
            "ICAR guidelines. See " +
            "https://www.icar.org/Guidelines/05-Conformation-Recording.pdf",
            "example": "BodyLength",
        },
    )
    method: Optional[icarEnums.icarConformationScoringMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "Method of conformation scoring",
            "example": "Automated",
        },
    )
    device: Optional[mongo_object_id.MongoObjectId] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for "
            + "the automated scoring.",
            "example": str(ObjectId()),
        },
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "description": "Time when conformation recorded. " +
            "Current time inserted if empty",
            "example": str(datetime.now()),
        },
    )


class ConformationCollection(BaseModel):
    conformation: List[Conformation]


@router.post(
    "/",
    response_description="Add conformation event",
    response_model=Conformation,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_conformation_event(request: Request,
                                    conformation: Conformation):
    """
    Create a new conformation event.

    :param conformation: Conformation to be added
    """
    model = conformation.model_dump(by_alias=True, exclude=["ft"])
    if model["timestamp"] is None:
        model["timestamp"] = datetime.now()
    try:
        new_ce = await request.app.state.conformation.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail="Conformation already exists")
    if (
        created_conformation_event :=
        await request.app.state.conformation.find_one(
            {"_id": new_ce.inserted_id}
        )
    ) is not None:
        return created_conformation_event
    raise HTTPException(
        status_code=404, detail="Conformation event not successfully added"
    )


@router.delete("/{ft}", response_description="Delete a conformation event")
async def remove_conformation_event(request: Request, ft: str):
    """
    Delete a conformation event.

    :param ft: ObjectID of the conformation event to delete
    """
    delete_result = await request.app.state.conformation.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Conformation event {ft} not found")


@router.get(
    "/",
    response_description="Search for conformation event",
    response_model=ConformationCollection,
    response_model_by_alias=False,
)
async def conformation_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: mongo_object_id.MongoObjectId | None = None,
    start: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    end: Annotated[datetime, Query(default_factory=datetime.now)] = None,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
):
    """Search for a conformation event given the provided criteria."""
    query = {
        "_id": ft,
        "animal": animal,
        "timestamp": {"$gte": start, "$lte": end},
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd},
    }
    result = await request.app.state.conformation.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return ConformationCollection(conformation=result)
    raise HTTPException(status_code=404, detail="No match found")
