"""
Collects API calls related to medicine.

This collection of endpoints allows for the addition, deletion
and finding of medicines.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                        find_in_db, update_one_in_db)
from ..icar.icarResources import icarMedicineResource as Medicine

router = APIRouter(
    prefix="/medicine",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Medicine"


class MedicineCollection(BaseModel):
    medicine: List[Medicine]


@router.post(
    "/",
    response_description="Add new medicine",
    response_model=Medicine,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_medicine(request: Request, medicine: Medicine):
    """
    Create a new medicine.

    :param medicine: Medicine to be added
    """
    return await add_one_to_db(medicine, request.app.state.medicine, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a medicine")
async def remove_medicine(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a medicine.

    :param ft: UUID of the medicine to delete
    """
    return await delete_one_from_db(request.app.state.medicine, ft, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update a medicine",
    response_model=Medicine,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_medicine(
    request: Request, ft: mongo_object_id.MongoObjectId, medicine: Medicine
):
    """
    Update an existing medicine if it exists.

    :param ft: UUID of the medicine to update
    :param medicine: Medicine to update with
    """
    return await update_one_in_db(
        medicine, request.app.state.medicine, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for medicine",
    response_model=MedicineCollection,
    response_model_by_alias=False,
)
async def medicine_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    name: str | None = None,
    approved: str | None = None,
    registeredID: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
):
    """Search for a medicine given the provided criteria."""
    query = {
        "_id": ft,
        "name": name,
        "approved": approved,
        "registeredID.id": registeredID,
        "modified": dateBuild(modifiedStart, modifiedEnd),
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.medicine, query)
    return MedicineCollection(medicine=result)
