"""
Collects API calls related to animals.

Animals are living things present on the farm.

An animal may have several devices attached to it.

An on-farm example is a single dairy cow, Hilda.

This collection of endpoints allows for the addition, deletion
and finding of those animals.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarAnimalCoreResource.json
"""
from fastapi import status, HTTPException, Response, APIRouter, Request, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from bson.objectid import ObjectId
from typing_extensions import Annotated
from pydantic_extra_types import mongo_object_id
from datetime import datetime
from ..icar import icarEnums, icarTypes
from ..ftCommon import FTModel, filterQuery

router = APIRouter(
    prefix="/animals",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


class Animal(FTModel):
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

    breedFractions: Optional[icarTypes.icarBreedFractions] = Field(
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
        animal.model_dump(by_alias=True, exclude=["ft"])
    )

    if (
        created_animal := await
        request.app.state.animals.find_one({"_id": new_animal.inserted_id})
    ) is not None:
        return created_animal
    raise HTTPException(status_code=404,
                        detail="Animal not successfully added")


@router.delete("/{ft}", response_description="Delete an animal")
async def remove_animal(request: Request, ft: str):
    """
    Delete an animal.

    :param id: UUID of the animal to delete
    """
    delete_result = await request.app.state.animals.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Animal {ft} not found")


@router.patch(
    "/{ft}",
    response_description="Update an animal",
    response_model=Animal,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_animal(request: Request, ft: str, animal: Animal):
    """
    Update an existing animal if it exists.

    :param id: UUID of the animal to update
    :param animal: Animal to update with
    """
    await request.app.state.animals.update_one(
        {"_id": ObjectId(ft)},
        {'$set': animal.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False
    )

    if (
        updated_animal := await
        request.app.state.animals.find_one({"_id": ObjectId(ft)})
    ) is not None:
        return updated_animal
    raise HTTPException(status_code=404,
                        detail=f"Animal {ft} not successfully updated")


@router.get(
    "/",
    response_description="Search for animals",
    response_model=AnimalCollection,
    response_model_by_alias=False,
)
async def animal_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    identifier: str | None = None,
    alternativeIdentifiers: Annotated[list[str] | None, Query()] = [],
    specie: icarEnums.icarAnimalSpecieType | None = None,
    gender: icarEnums.icarAnimalGenderType | None = None,
    birthDateStart: datetime | None = datetime(
        1970, 1, 1, 0, 0, 0),
    birthDateEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    primaryBreed: str | None = None,
    coatColor: str | None = None,
    coatColorIdentifier: str | None = None,
    managementTag: str | None = None,
    name: str | None = None,
    officialName: str | None = None,
    productionPurpose: icarEnums.icarProductionPurposeType | None = None,
    status: icarEnums.icarAnimalStatusType | None = None,
    reproductionStatus: icarEnums.icarAnimalReproductionStatusType | None = None,
    lactationStatus: icarEnums.icarAnimalLactationStatusType | None = None,
    parentage: Annotated[list[str] | None, Query()] = [],
    healthStatus: icarEnums.icarAnimalHealthStatusType | None = None,
    createdStart: datetime | None = datetime(
        1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    modifiedStart: datetime | None = datetime(
        1970, 1, 1, 0, 0, 0),
    modifiedEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None
):
    """
    Search for an animal given the provided criteria.
    """
    query = {
        "_id": ft,
        "identifier": identifier,
        "specie": specie,
        "gender": gender,
        "primaryBreed": primaryBreed,
        "coatColor": coatColor,
        "coatColorIdentifier": coatColorIdentifier,
        "managementTag": managementTag,
        "birthDate": {"$gte": birthDateStart, "$lte": birthDateEnd},
        "name": name,
        "officialName": officialName,
        "productionPurpose": productionPurpose,
        "alternativeIdentifiers": {"$in": alternativeIdentifiers},
        "status": status,
        "reproductionStatus": reproductionStatus,
        "lactationStatus": lactationStatus,
        "parentage": {"$in": parentage},
        "healthStatus": healthStatus,
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": modifiedStart, "$lte": modifiedEnd}
    }
    result = await request.app.state.animals.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return AnimalCollection(animals=result)
    else:
        raise HTTPException(status_code=404, detail="No match found")
