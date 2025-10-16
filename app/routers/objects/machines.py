"""
Collects API calls related to machines.

A machine is an item of equipment, a vehicle, an attachment, etc.

A machine may have several devices attached to it.

An on-farm example is a Tractor.

This collection of endpoints allows for the addition, deletion
and finding of those machines.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query, Request, Security, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import FTModel, add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/machines",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Machine"


class Machine(FTModel):
    manufacturer: str = Field(
        json_schema_extra={
            "description": "Manufacturer of machine",
            "example": "Acme Machine Co.",
        }
    )
    model: str = Field(
        json_schema_extra={
            "description": "Model number or product code of device",
            "example": "Machine 3000",
        }
    )
    type: Optional[list[str]] = Field(
        json_schema_extra={
            "description": "List of categories to which this machine belongs",
            "example": '["Tractor", "Utility"]',
        }
    )
    registration: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Assigned vehicle registration number, if applicable",
            "example": "BD51 SMR",
        },
    )


class MachineCollection(BaseModel):
    machines: List[Machine]


@router.post(
    "/",
    response_description="Add new machine",
    response_model=Machine,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_machine(
    request: Request,
    machine: Machine,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_machine"])
    ],
):
    """
    Create a new machine.

    :param machine: Machine to be added
    """
    return await add_one_to_db(machine, request.app.state.machines, ERROR_MSG_OBJECT)


@router.delete("/{ft}", response_description="Delete a machine")
async def remove_machine(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_machine"])
    ],
):
    """
    Delete an machine.

    :param ft: UUID of the machine to delete
    """
    return await delete_one_from_db(request.app.state.machines, ft, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update an machine",
    response_model=Machine,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_machine(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    machine: Machine,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_machine"])
    ],
):
    """
    Update an existing machine if it exists.

    :param ft: UUID of the machine to update
    :param machine: Machine to update with
    """
    await request.app.state.machines.update_one(
        {"_id": ObjectId(ft)},
        {"$set": machine.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False,
    )

    if (
        updated_machine := await request.app.state.machines.find_one(
            {"_id": ObjectId(ft)}
        )
    ) is not None:
        return updated_machine
    raise HTTPException(
        status_code=404, detail=f"Machine {ft} not successfully updated"
    )


@router.get(
    "/",
    response_description="Search for machines",
    response_model=MachineCollection,
    response_model_by_alias=False,
)
async def machine_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_machine"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    manufacturer: str | None = None,
    model: str | None = None,
    type: Annotated[list[str] | None, Query()] = [],
    registration: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """
    Search for a machine given the provided criteria.

    :param ft: Object ID of the machine
    :param manufacturer: Manufacturer of the machine(s)
    :param model: Model of the machine(s)
    :param type: Type of the machine(s)
    :param registration: Registration mark/number of the machine
    """

    query = {
        "_id": ft,
        "manufacturer": manufacturer,
        "model": model,
        "registration": registration,
        "type": {"$in": type},
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.machines, query)
    return MachineCollection(machines=result)
