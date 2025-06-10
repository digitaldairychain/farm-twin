"""
Collects API calls related to withdrawal events.

A withdrawal resource used to indicate that product should be separated
(e.g. colostrum from newly lactating cows).

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarWithdrawalEventResource.json
"""
from datetime import datetime
from typing import List

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import filterQuery
from ..icar import icarEnums
from .eventCommon import AnimalEventModel

router = APIRouter(
    prefix="/withdrawal",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


class Withdrawal(AnimalEventModel):
    endDateTime: datetime = Field(
        json_schema_extra={
            "description": "RFC3339 UTC date and time " +
            "(see https://ijmacd.github.io/rfc3339-iso8601/)."
        }
    )
    productType: icarEnums.icarWithdrawalProductType = Field(
        json_schema_extra={
            "description": "Product or food item affected by this withdrawal.",
        },
    )


class WithdrawalCollection(BaseModel):
    withdrawal: List[Withdrawal]


@router.post(
    "/",
    response_description="Add withdrawal event",
    response_model=Withdrawal,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_withdrawal_event(request: Request, withdrawal: Withdrawal):
    """
    Create a new withdrawal event.

    :param withdrawal: Withdrawal to be added
    """
    model = withdrawal.model_dump(by_alias=True, exclude=["ft"])
    try:
        new_we = await request.app.state.withdrawal.insert_one(model)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail=f"Withdrawal {withdrawal} already exists")
    if (
        created_withdrawal_event :=
        await request.app.state.withdrawal.find_one(
            {"_id": new_we.inserted_id}
        )
    ) is not None:
        return created_withdrawal_event
    raise HTTPException(
        status_code=404, detail="Withdrawal event not successfully added"
    )


@router.delete("/{ft}", response_description="Delete a withdrawal event")
async def remove_withdrawal_event(request: Request, ft: str):
    """
    Delete a withdrawal event.

    :param ft: ObjectID of the withdrawal event to delete
    """
    delete_result = await request.app.state.withdrawal.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Withdrawal event {ft} not found")


@router.get(
    "/",
    response_description="Search for withdrawal event",
    response_model=WithdrawalCollection,
    response_model_by_alias=False,
)
async def withdrawal_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: mongo_object_id.MongoObjectId | None = None,
    start: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    end: Annotated[datetime, Query(default_factory=datetime.now)] = None,
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
):
    """Search for a withdrawal event given the provided criteria."""
    query = {
        "_id": ft,
        "animal": animal,
        "endDateTime": {"$gte": start, "$lte": end},
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": createdStart, "$lte": createdEnd},
    }
    result = await request.app.state.withdrawal.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return WithdrawalCollection(withdrawal=result)
    raise HTTPException(status_code=404, detail="No match found")
