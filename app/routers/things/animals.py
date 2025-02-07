from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/animals",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Animal(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    eid: Optional[str] = Field(default=None)


class AnimalCollection(BaseModel):
    animals: List[Animal]


@router.post(
    "/",
    response_description="Add new animal",
    response_model=Animal,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_animal(request: Request, animal: Animal):
    new_animal = await request.app.state.animals.insert_one(
        animal.model_dump(by_alias=True, exclude=["id"])
    )

    if (
        created_animal := await
        request.app.state.animals.find_one({"_id": new_animal.inserted_id})
    ) is not None:
        return created_animal
    raise HTTPException(status_code=404,
                        detail=f"Animal {id} not successfully added")


@router.delete("/{id}", response_description="Delete a animal")
async def remove_animal(request: Request, id: str):
    delete_result = await request.app.state.animals.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Animal {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single animal",
    response_model=Animal,
    response_model_by_alias=False,
)
async def list_animal_single(request: Request, id: str):
    if (
        animal := await request.app.state.animals.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return animal

    raise HTTPException(status_code=404, detail=f"Animal {id} not found")


@router.get(
    "/",
    response_description="List all animals",
    response_model=AnimalCollection,
    response_model_by_alias=False,
)
async def list_animal_collection(request: Request):
    return AnimalCollection(animals=await
                            request.app.state.animals.find().to_list(1000))
