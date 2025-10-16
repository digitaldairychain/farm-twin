"""
Collects API calls related to polygons.

A polygon is a series of static locations expressed in two dimensions.
By drawing lines between each of these, a shape can be drawn which
describes an area.

An area may have several devices attached/within to it.

An on-farm example is an animal pen within a shed.

This collection of endpoints allows for the addition, deletion
and finding of those points.
"""

import uuid
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Request, Response, Security, status
from geojson_pydantic import FeatureCollection, MultiPolygon
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import add_one_to_db, delete_one_from_db
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/polygons",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Polygons"


class Polygon(BaseModel):
    id: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            "description": "UUID of polygon",
            "example": str(uuid.uuid4()),
        },
    )
    polygon: MultiPolygon = Field(
        json_schema_extra={
            "description": "GeoJSON MultiPolygon, a bounded shape on earth"
        }
    )
    tags: Optional[List[str]] = Field(default=[])


@router.post(
    "/",
    response_description="Add new polygon",
    response_model=Polygon,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_polygon(
    request: Request,
    polygon: Polygon,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_polygons"])
    ],
):
    """
    Create a new polygon.

    :param polygon: Polygon to be added
    """
    return await add_one_to_db(polygon, request.app.state.polygons, ERROR_MSG_OBJECT)


@router.delete("/{id}", response_description="Delete a polygon")
async def remove_polygon(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_polygons"])
    ],
):
    """
    Delete a polygon.

    :param id: UUID of the polygon to delete
    """
    return await delete_one_from_db(request.app.state.polygons, ft, ERROR_MSG_OBJECT)


@router.get(
    "/",
    response_description="Search for polygon",
    response_model=FeatureCollection,
    response_model_by_alias=False,
)
async def polygon_query(
    request: Request,
    response: Response,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_polygons"])
    ],
    id: str | None = None,
    tag: str | None = None,
):
    """
    Search for a polygon given the provided criteria.

    :param id: Object ID of the polygon
    :param tag: Tag of the polygon
    """
    query = {}
    if id:
        query["_id"] = mongo_object_id.MongoObjectId(id)
    if tag:
        query["tags"] = {"$in": [tag]}
    result = await request.app.state.polygons.find(query).to_list(1000)
    if len(result) > 0:
        fc = {"type": "FeatureCollection", "features": []}
        for polygon in result:
            f = {
                "type": "Feature",
                "properties": {
                    "objectid": str(polygon["_id"]),
                    "tags": polygon["tags"],
                    "type": "polygon",
                },
                "geometry": polygon["polygon"],
            }
            fc["features"].append(f)
            response.headers["Access-Control-Allow-Origin"] = "*"
        return fc
    raise HTTPException(status_code=404, detail="No match found")


# TODO: Allow searching within a bounded box
