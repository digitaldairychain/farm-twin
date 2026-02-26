"""
Collects API calls related to image metadata.

This collection of endpoints allows for the addition, deletion
and finding of that metadata.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import FTModel, add_one_to_db, delete_one_from_db, find_in_db
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/metadata",
    tags=["imagery"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Metadata"


class Metadata(FTModel):
    image: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of image",
            "example": str(mongo_object_id.MongoObjectId()),
        }
    )
    metadata: Dict[str, Any] = Field(
        default=None,
        json_schema_extra={"description": "Metadata relating to the image"},
    )


class MetadataCollection(BaseModel):
    metadata: List[Metadata]


@router.post(
    "/",
    response_description="Add new metadata",
    response_model=Metadata,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_metadata(
    request: Request,
    metadata: Metadata,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_imagery"])
    ],
):
    """
    Creat new metadata if it does not already exist.

    :param metadata: Metadata to be added
    """
    return await add_one_to_db(
        metadata, request.app.state.metadata, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete metadata")
async def remove_metadata(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_imagery"])
    ],
):
    """
    Delete metadata.

    :param ft: ObjectID of the metadata to delete
    """
    return await delete_one_from_db(
        request.app.state.metadata, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for metadata",
    response_model=MetadataCollection,
    response_model_by_alias=False,
)
async def metadata_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_imagery"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    image: mongo_object_id.MongoObjectId | None = None,
):
    """Search for a metadata given the provided criteria."""
    query = {
        "_id": ft,
        "image": image,
    }
    result = await find_in_db(request.app.state.metadata, query)
    return MetadataCollection(metadata=result)
