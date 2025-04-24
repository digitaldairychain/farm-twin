"""
Collects API calls related to animals.

Animals are living things present on the farm.

An animal may have several devices attached to it.

An on-farm example is a single dairy cow, Hilda.

This collection of endpoints allows for the addition, deletion
and finding of those animals.

Compliant with ICAR data standards: https://github.com/adewg/ICAR/tree/ADE-1
"""
from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId
from datetime import datetime
from . import icarEnums

router = APIRouter(
    prefix="/animals",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)

PyObjectId = Annotated[str, BeforeValidator(str)]


class Fraction(BaseModel):
    breed: str
    fraction: float


class BreedFraction(BaseModel):
    denominator: int
    fractions: List[Fraction]


class Animal(BaseModel):
    id: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            'description': 'UUID of animal',
            'example': str(ObjectId())
        }
    )

    identifier: str = Field(
        json_schema_extra={
            'description': 'Unique animal scheme and identifier combination.',
            'example': 'UK230011200123'
        }
    )

    alternativeIdentifier: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            'description': 'Alternative identifiers for the animal. ' +
            'Here, also temporary identifiers, e.g. transponders or animal ' +
            'numbers, can be listed.',
        }
    )

    specie: icarEnums.icarAnimalSpecieType = Field(
        json_schema_extra={
            'description': 'Species of the animal.',
            'example': 'Cattle'
        }
    )

    gender: icarEnums.icarAnimalGenderType = Field(
        json_schema_extra={
            'description': 'Gender of the animal.',
            'example': 'Female'
        }
    )

    birthDate: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            'description': 'Date and time of birth.',
            'example': str(datetime.now())
        }
    )

    primaryBreed: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'ICAR Breed code for the animal.',
            'example': 'HOL'
        }
    )

    breedFractions: Optional[BreedFraction] = Field(
        default=None,
        json_schema_extra={
            'description': 'Breed fractions for the animal.',
        }
    )

    coatColor: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': "Colour of the animal's coat, using the " +
            "conventions for that breed.",
        }
    )

    coatColorIdentifier: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': "Colour of the animal's coat using a national " +
            "or breed-defined scheme and identifier combination.",
        }
    )

    managementTag: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'The identifier used by the farmer in day to day ' +
            'operations. In many cases this could be the animal number.',
        }
    )

    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'Name given by the farmer for this animal.',
        }
    )

    officialName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'Official herdbook name.',
        }
    )

    productionPurpose: Optional[icarEnums.icarProductionPurposeType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Primary production purpose for which animals ' +
            'are bred.',
            'example': 'Milk'
        }
    )

    status: Optional[icarEnums.icarAnimalStatusType] = Field(
        default=None,
        json_schema_extra={
            'description': 'On-farm status of the animal.',
            'example': 'Alive'
        }
    )

    reproductionStatus: Optional[icarEnums.icarAnimalReproductionStatusType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Reproduction status of the animal.',
            'example': 'Pregnant'
        }
    )

    lactationStatus: Optional[icarEnums.icarAnimalLactationStatusType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Lactation status of the animal.',
            'example': 'Fresh'
        }
    )

    parentage: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            'description': 'Parents of the animal.  The array can handle ' +
            'multiple generations by specifying the parent of a parent.',
        }
    )

    healthStatus: Optional[icarEnums.icarAnimalHealthStatusType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Health status of the animal',
            'example': 'InTreatment'
        }
    )


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
    """
    Create a new animal.

    :param animal: Animal to be added
    """
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


@router.delete("/{id}", response_description="Delete an animal")
async def remove_animal(request: Request, id: str):
    """
    Delete an animal.

    :param id: UUID of the animal to delete
    """
    delete_result = await request.app.state.animals.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Animal {id} not found")


@router.patch(
        "/{id}",
        response_description="Update an animal",
        response_model=Animal,
        status_code=status.HTTP_202_ACCEPTED
    )
async def update_animal(request: Request, id: str, animal: Animal):
    """
    Update an existing animal if it exists.

    :param id: UUID of the animal to update
    :param animal: Animal to update with
    """
    await request.app.state.animals.update_one(
        {"_id": ObjectId(id)},
        {'$set': animal.model_dump(by_alias=True, exclude=["id"])},
        upsert=False
    )

    if (
        updated_animal := await
        request.app.state.animals.find_one({"_id": ObjectId(id)})
    ) is not None:
        return updated_animal
    raise HTTPException(status_code=404,
                        detail=f"Animal {id} not successfully updated")


@router.get(
    "/",
    response_description="Search for animals",
    response_model=AnimalCollection,
    response_model_by_alias=False,
)
async def animal_query(request: Request,
                       id: str | None = None,
                       eid: str | None = None):
    """
    Search for an animal given the provided criteria.

    :param id: Object ID of the animal
    :param eid: Electronic identification tag number of animal
    """
    if id:
        id = ObjectId(id)
    query = {
        "_id": id,
        "eid": eid,
        }
    filtered_query = {k: v for k, v in query.items() if v is not None}
    result = await request.app.state.animals.find(filtered_query).to_list(1000)
    if len(result) > 0:
        return AnimalCollection(animals=result)
    raise HTTPException(status_code=404, detail="No match found")
