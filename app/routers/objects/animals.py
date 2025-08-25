"""
Collects API calls related to animals.

Animals are living things present on the farm.

An animal may have several devices attached to it.

An on-farm example is a single dairy cow, Hilda.

This collection of endpoints allows for the addition, deletion
and finding of those animals.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarAnimalCoreResource.json
"""

from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import dateBuild, filterQuery
from ..icar import icarEnums, icarTypes
from ..icar.icarResources import icarAnimalCoreResource as Animal

router = APIRouter(
    prefix="/animals",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
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
        animal.model_dump(by_alias=True, exclude=["ft", "resourceType"])
    )

    if (
        created_animal := await request.app.state.animals.find_one(
            {"_id": new_animal.inserted_id}
        )
    ) is not None:
        return created_animal
    raise HTTPException(
        status_code=404, detail="Animal not successfully added")


@router.delete("/{ft}", response_description="Delete an animal")
async def remove_animal(request: Request, ft: str):
    """
    Delete an animal.

    :param id: UUID of the animal to delete
    """
    delete_result = await request.app.state.animals.delete_one({"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Animal {ft} not found")


@router.patch(
    "/{ft}",
    response_description="Update an animal",
    response_model=Animal,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_animal(request: Request, ft: str, animal: Animal):
    """
    Update an existing animal if it exists.

    :param id: UUID of the animal to update
    :param animal: Animal to update with
    """
    await request.app.state.animals.update_one(
        {"_id": ObjectId(ft)},
        {"$set": animal.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False,
    )

    if (
        updated_animal := await request.app.state.animals.find_one(
            {"_id": ObjectId(ft)}
        )
    ) is not None:
        return updated_animal
    raise HTTPException(
        status_code=404, detail=f"Animal {ft} not successfully updated")


@router.get(
    "/",
    response_description="Search for animals",
    response_model=AnimalCollection,
    response_model_by_alias=False,
)
async def animal_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    identifier: icarTypes.icarAnimalIdentifierType | None = None,
    alternativeIdentifiers: Annotated[list[str] | None, Query()] = [],
    specie: icarEnums.icarAnimalSpecieType | None = None,
    gender: icarEnums.icarAnimalGenderType | None = None,
    birthDateStart: datetime | None = None,
    birthDateEnd: datetime | None = None,
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
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
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
        "birthDate": dateBuild(birthDateStart, birthDateEnd),
        "name": name,
        "officialName": officialName,
        "productionPurpose": productionPurpose,
        "alternativeIdentifiers": {"$in": alternativeIdentifiers},
        "status": status,
        "reproductionStatus": reproductionStatus,
        "lactationStatus": lactationStatus,
        "parentage": {"$in": parentage},
        "healthStatus": healthStatus,
        "created": dateBuild(createdStart, createdEnd),
        "modified": dateBuild(modifiedStart, modifiedEnd),
    }
    result = await request.app.state.animals.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return AnimalCollection(animals=result)
    else:
        raise HTTPException(status_code=404, detail="No match found")
