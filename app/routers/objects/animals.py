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

from fastapi import APIRouter, Query, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
    update_one_in_db,
)
from ..icar import icarEnums, icarTypes
from ..icar.icarResources import icarAnimalCoreResource as Animal
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/animals",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Animal"


class AnimalCollection(BaseModel):
    animals: List[Animal]


@router.post(
    "/",
    response_description="Add new animal",
    response_model=Animal,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_animal(
    request: Request,
    animal: Animal,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_animals"])
    ],
):
    """
    Create a new animal.

    :param animal: Animal to be added
    """
    return await add_one_to_db(
        animal, request.app.state.animals, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete an animal")
async def remove_animal(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_animals"])
    ],
):
    """
    Delete an animal.

    :param id: UUID of the animal to delete
    """
    return await delete_one_from_db(
        request.app.state.animals, ft, ERROR_MSG_OBJECT
    )


@router.patch(
    "/{ft}",
    response_description="Update an animal",
    response_model=Animal,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_animal(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    animal: Animal,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_animals"])
    ],
):
    """
    Update an existing animal if it exists.

    :param id: UUID of the animal to update
    :param animal: Animal to update with
    """
    return await update_one_in_db(
        animal, request.app.state.animals, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for animals",
    response_model=AnimalCollection,
    response_model_by_alias=False,
)
async def animal_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_animals"])
    ],
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
    reproductionStatus: icarEnums.icarAnimalReproductionStatusType
    | None = None,
    lactationStatus: icarEnums.icarAnimalLactationStatusType | None = None,
    parentage: Annotated[list[str] | None, Query()] = [],
    healthStatus: icarEnums.icarAnimalHealthStatusType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
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
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.animals, query)
    return AnimalCollection(animals=result)
