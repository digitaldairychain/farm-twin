"""
Collects API calls related to points.

A point is a single fixed static location expressed in two dimensions.

A point may have several devices attached to it.

An on-farm example is a stake inserted into the ground in a field.

This collection of endpoints allows for the addition, deletion
and finding of those points.
"""
import pymongo
import uuid

from fastapi import status, HTTPException, Response, APIRouter, Request, Response
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional
from typing_extensions import Annotated
from geojson_pydantic import Point, FeatureCollection
from bson.objectid import ObjectId


router = APIRouter(
    prefix="/points",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Point(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, json_schema_extra={
        'description': 'UUID of point',
        'example': str(uuid.uuid4())})
    point: Point = Field(json_schema_extra={
        'description': 'GeoJSON Point, used to describe a point on the ground, such as a fixed post in the ground'})


@router.post(
    "/",
    response_description="Add new point",
    response_model=Point,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_point(request: Request, point: Point):
    """
    Create a new point.

    :param point: Point to be added
    """
    try:
        new_point = await request.app.state.points.insert_one(
            point.model_dump(by_alias=True, exclude=["id"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail=f"Point {point} already exists")
    if (
        created_point := await
        request.app.state.points.find_one({"_id": new_point.inserted_id})
    ) is not None:
        return created_point
    raise HTTPException(status_code=404, detail=f"Point {point._id}" +
                        " not successfully added")


@router.delete("/{id}", response_description="Delete a point")
async def remove_point(request: Request, id: str):
    """
    Delete a point.

    :param id: UUID of the point to delete
    """
    delete_result = await request.app.state.points.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Point {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single point",
    response_model=Point,
    response_model_by_alias=False,
)
async def list_point_single(request: Request, id: str):
    """
    Fetch a single point.

    :param id: UUID of the point to fetch details of
    """
    if (
        point := await request.app.state.points.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return point

    raise HTTPException(status_code=404, detail=f"Point {id} not found")


@router.get(
    "/bycoordinate/",
    response_description="Get a point by coordinates",
    response_model=Point,
    response_model_by_alias=False,
)
async def list_point_coordinates(request: Request, lat: float, long: float):
    """
    Fetch a single point at a specific coordinate.

    :param lat: Latititude of point
    :param long: Longitude of point
    """
    coordinate = {"bbox": None, "type": "Point", "coordinates": [lat, long]}
    if (
        point := await request.app.state.points.find_one(
            {"point": coordinate})
    ) is not None:
        return point

    raise HTTPException(status_code=404,
                        detail=f"Point not found {coordinate}")


@router.get(
    "/",
    response_description="List all points",
    response_model=FeatureCollection,
    response_model_by_alias=False,
)
async def list_point_collection(request: Request, response: Response):
    """Fetch all current points."""
    fc = {"type": "FeatureCollection", "features": []}
    points = await request.app.state.points.find().to_list(1000)
    for point in points:
        f = {
             "type": "Feature",
             "properties": {
                 "objectid": str(point["_id"])
             },
             "geometry": point["point"]
            }
        fc["features"].append(f)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return fc
