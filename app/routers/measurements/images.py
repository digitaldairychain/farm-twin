"""
Collects API calls related to earth observation image metadata.

Earth observation image metadata records information about satellite imagery
captured over farm locations.

An image is captured by a satellite platform and instrument and may be
associated with a farm polygon (area of interest).

An on-farm example is a Sentinel-2 multispectral image captured over a
field to monitor crop health.

This collection of endpoints allows for the addition, deletion
and finding of earth observation image metadata records.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import (
    FTModel,
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
)
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/images",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Image"


class ImageMetadata(FTModel):
    platform: str = Field(
        json_schema_extra={
            "description": "Name of the satellite platform that captured the image",
            "example": "Sentinel-2A",
        }
    )
    instrument: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name of the sensor or instrument on the platform",
            "example": "MSI",
        },
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            "description": "Acquisition time of the image",
            "example": str(datetime.now()),
        },
    )
    uri: str = Field(
        json_schema_extra={
            "description": "URI or path to the image file or data product",
            "example": "https://example.com/eo/sentinel2-20250101.tif",
        }
    )
    location: Optional[mongo_object_id.MongoObjectId] = Field(
        default=None,
        json_schema_extra={
            "description": "ObjectID of the farm polygon (area of interest) covered by the image",
            "example": str(mongo_object_id.MongoObjectId()),
        },
    )
    resolution: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Spatial resolution of the image in metres",
            "example": 10.0,
        },
    )
    cloudCover: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Percentage of the image obscured by cloud cover (0-100)",
            "example": 5.2,
        },
    )
    bands: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "description": "List of spectral bands available in the image",
            "example": ["B02", "B03", "B04", "B08"],
        },
    )


class ImageMetadataCollection(BaseModel):
    images: List[ImageMetadata]


@router.post(
    "/",
    response_description="Add new earth observation image metadata",
    response_model=ImageMetadata,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_image(
    request: Request,
    image: ImageMetadata,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_measurements"])
    ],
):
    """
    Create a new earth observation image metadata record.

    :param image: Image metadata to be added
    """
    return await add_one_to_db(
        image, request.app.state.images, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete earth observation image metadata")
async def remove_image(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_measurements"])
    ],
):
    """
    Delete an earth observation image metadata record.

    :param ft: ObjectID of the image metadata to delete
    """
    return await delete_one_from_db(
        request.app.state.images, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for earth observation image metadata",
    response_model=ImageMetadataCollection,
    response_model_by_alias=False,
)
async def image_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_measurements"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    platform: str | None = None,
    instrument: str | None = None,
    location: mongo_object_id.MongoObjectId | None = None,
    timestampStart: datetime | None = None,
    timestampEnd: datetime | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for earth observation image metadata given the provided criteria."""
    query = {
        "_id": ft,
        "platform": platform,
        "instrument": instrument,
        "location": location,
        "timestamp": dateBuild(timestampStart, timestampEnd),
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.images, query)
    return ImageMetadataCollection(images=result)
