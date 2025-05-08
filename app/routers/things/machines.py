"""
Collects API calls related to machines.

A machine is an item of equipment, a vehicle, an attachment, etc.

A machine may have several devices attached to it.

An on-farm example is a Tractor.

This collection of endpoints allows for the addition, deletion
and finding of those machines.
"""
from fastapi import status, HTTPException, Response, APIRouter, Request, Query
from pydantic import BaseModel, Field, AfterValidator
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId
from ..ftCommon import FTModel, checkObjectId, filterQuery

router = APIRouter(
    prefix="/machines",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Machine(FTModel):
    manufacturer: str = Field(json_schema_extra={
        'description': 'Manufacturer of machine',
        'example': 'Acme Machine Co.'})
    model: str = Field(json_schema_extra={
        'description': 'Model number or product code of device',
        'example': 'Machine 3000'})
    type: Optional[list[str]] = Field(json_schema_extra={
        'description': 'List of categories to which this machine belongs',
        'example': '["Tractor", "Utility"]'})
    registration: Optional[str] = Field(default=None, json_schema_extra={
        'description': 'Assigned vehicle registration number, if applicable',
        'example': 'BD51 SMR'})


class MachineCollection(BaseModel):
    machines: List[Machine]


@router.post(
    "/",
    response_description="Add new machine",
    response_model=Machine,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_machine(request: Request, machine: Machine):
    """
    Create a new machine.

    :param machine: Machine to be added
    """
    new_machine = await request.app.state.machines.insert_one(
        machine.model_dump(by_alias=True, exclude=["ft"])
    )
    if (
        created_machine := await
        request.app.state.machines.find_one({"_id": new_machine.inserted_id})
    ) is not None:
        return created_machine
    raise HTTPException(status_code=404,
                        detail="Machine not successfully added")


@router.delete("/{ft}", response_description="Delete a machine")
async def remove_machine(request: Request, ft: str):
    """
    Delete an machine.

    :param ft: UUID of the machine to delete
    """
    delete_result = await request.app.state.machines.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Machine {ft} not found")


@router.patch(
    "/{ft}",
    response_description="Update an machine",
    response_model=Machine,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_machine(request: Request, ft: str, machine: Machine):
    """
    Update an existing machine if it exists.

    :param ft: UUID of the machine to update
    :param machine: Machine to update with
    """
    await request.app.state.machines.update_one(
        {"_id": ObjectId(ft)},
        {'$set': machine.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False
    )

    if (
        updated_machine := await
        request.app.state.machines.find_one({"_id": ObjectId(ft)})
    ) is not None:
        return updated_machine
    raise HTTPException(status_code=404,
                        detail=f"Machine {ft} not successfully updated")


@router.get(
    "/",
    response_description="Search for machines",
    response_model=MachineCollection,
    response_model_by_alias=False,
)
async def machine_query(request: Request,
                        ft: Annotated[str | None, AfterValidator(
                            checkObjectId)] = None,
                        manufacturer: str | None = None,
                        model: str | None = None,
                        type: Annotated[list[str] | None, Query()] = [],
                        registration: str | None = None):
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
        "model":  model,
        "registration": registration,
        "type": {"$in": type}
    }
    result = await request.app.state.machines.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return MachineCollection(machines=result)
    raise HTTPException(status_code=404, detail="No match found")
