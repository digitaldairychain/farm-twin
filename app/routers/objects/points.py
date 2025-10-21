"""
Collects API calls related to points.

A point is a single fixed static location expressed in two dimensions.

A point may have several devices attached to it.

An on-farm example is a stake inserted into the ground in a field.

This collection of endpoints allows for the addition, deletion
and finding of those points.
"""

import uuid
from typing import List, Optional

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
    Security,
    status
)
from geojson_pydantic import FeatureCollection, Point
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import add_one_to_db, delete_one_from_db
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/points",
    tags=["objects"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Point"


class Point(BaseModel):
    id: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            "description": "UUID of point",
            "example": str(uuid.uuid4()),
        },
    )
    point: Point = Field(
        json_schema_extra={
            "description": "GeoJSON Point, a fixed point on earth"}
    )
    tags: Optional[List[str]] = Field(default=[])


@router.post(
    "/",
    response_description="Add new point",
    response_model=Point,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_point(
    request: Request,
    point: Point,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_points"])
    ],
):
    """
    Create a new point.

    :param point: Point to be added
    """
    return await add_one_to_db(
        point,
        request.app.state.points,
        ERROR_MSG_OBJECT
    )


@router.delete("/{id}", response_description="Delete a point")
async def remove_point(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_points"])
    ],
):
    """
    Delete a point.

    :param id: UUID of the point to delete
    """
    return await delete_one_from_db(
        request.app.state.points,
        ft,
        ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for points",
    response_model=FeatureCollection,
    response_model_by_alias=False,
)
async def point_query(
    request: Request,
    response: Response,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_points"])
    ],
    id: str | None = None,
    lat: float | None = None,
    long: float | None = None,
    tag: str | None = None,
):
    """
    Search for a point given the provided criteria.

    :param id: Object ID of the point
    :param lat: Latitude of point
    :param long: Longitude of point
    :param tag: Tag of the point
    """
    query = {}
    if id:
        query["_id"] = mongo_object_id.MongoObjectId(id)
    if tag:
        query["tags"] = {"$in": [tag]}
    if lat is not None and long is not None:
        query["point"] = {"bbox": None,
                          "type": "Point", "coordinates": [lat, long]}
    if tag:
        query["tags"] = {"$in": [tag]}
    result = await request.app.state.points.find(query).to_list(1000)
    if len(result) > 0:
        fc = {"type": "FeatureCollection", "features": []}
        for point in result:
            f = {
                "type": "Feature",
                "properties": {
                    "objectid": str(point["_id"]),
                    "tags": point["tags"],
                    "type": "point",
                },
                "geometry": point["point"],
            }
            fc["features"].append(f)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return fc
    raise HTTPException(status_code=404, detail="No match found")


# TODO: Allow searching within a bounded box
