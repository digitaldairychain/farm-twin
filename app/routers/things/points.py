"""
Collects API calls related to points.

A point is a single fixed static location expressed in two dimensions.

A point may have several devices attached to it.

An on-farm example is a stake inserted into the ground in a field.

This collection of endpoints allows for the addition, deletion
and finding of those points.
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from geojson_pydantic import Point
from bson.objectid import ObjectId


router = APIRouter(
    prefix="/points",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Point(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    point: Point
    tags: Optional[List[str]] = Field(default=[])


class PointCollection(BaseModel):
    points: List[Point]


@router.post(
    "/",
    response_description="Add new point",
    response_model=Point,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_point(request: Request, point: Point):
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
    response_model=PointCollection,
    response_model_by_alias=False,
)
async def list_point_collection(request: Request, ):
    return PointCollection(points=await
                           request.app.state.points.find().to_list(1000))
