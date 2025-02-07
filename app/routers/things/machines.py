from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/machines",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Machine(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    manufacturer: str
    model: str
    registration: Optional[str] = Field(default=None)


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
    new_machine = await request.app.state.machines.insert_one(
        machine.model_dump(by_alias=True, exclude=["id"])
    )

    if (
        created_machine := await
        request.app.state.machines.find_one({"_id": new_machine.inserted_id})
    ) is not None:
        return created_machine
    raise HTTPException(status_code=404,
                        detail=f"Machine {id} not successfully added")


@router.delete("/{id}", response_description="Delete a machine")
async def remove_machine(request: Request, id: str):
    delete_result = await request.app.state.machines.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Machine {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single machine",
    response_model=Machine,
    response_model_by_alias=False,
)
async def list_machine_single(request: Request, id: str):
    if (
        machine := await request.app.state.machines.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return machine

    raise HTTPException(status_code=404, detail=f"Machine {id} not found")


@router.get(
    "/",
    response_description="List all machines",
    response_model=MachineCollection,
    response_model_by_alias=False,
)
async def list_machine_collection(request: Request):
    return MachineCollection(machines=await
                             request.app.state.machines.find().to_list(1000))
