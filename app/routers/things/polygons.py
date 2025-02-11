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
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from geojson_pydantic import Polygon
from bson.objectid import ObjectId


router = APIRouter(
    prefix="/polygons",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Polygon(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    polygon: Polygon
    tags: Optional[List[str]] = Field(default=[])


class PolygonCollection(BaseModel):
    polygons: List[Polygon]


@router.post(
    "/",
    response_description="Add new polygon",
    response_model=Polygon,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_polygon(request: Request, polygon: Polygon):
    try:
        new_polygon = await request.app.state.polygons.insert_one(
            polygon.model_dump(by_alias=True, exclude=["id"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail=f"Polygon {polygon} already exists")
    if (
        created_polygon := await
        request.app.state.polygons.find_one({"_id": new_polygon.inserted_id})
    ) is not None:
        return created_polygon
    raise HTTPException(status_code=404, detail=f"Polygon {polygon._id}" +
                        " not successfully added")


@router.delete("/{id}", response_description="Delete a polygon")
async def remove_polygon(request: Request, id: str):
    delete_result = await request.app.state.polygons.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Polygon {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single polygon",
    response_model=Polygon,
    response_model_by_alias=False,
)
async def list_polygon_single(request: Request, id: str):
    if (
        polygon := await request.app.state.polygons.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return polygon

    raise HTTPException(status_code=404, detail=f"Polygon {id} not found")


@router.get(
    "/bycoordinate/",
    response_description="Get a polygon by coordinates",
    response_model=Polygon,
    response_model_by_alias=False,
)
async def list_polygon_coordinates(request: Request, lat: float, long: float):
    coordinate = {"bbox": None, "type": "Polygon", "coordinates": [lat, long]}
    if (
        polygon := await request.app.state.polygons.find_one(
            {"polygon": coordinate})
    ) is not None:
        return polygon

    raise HTTPException(status_code=404,
                        detail=f"Polygon not found {coordinate}")


@router.get(
    "/",
    response_description="List all polygons",
    response_model=PolygonCollection,
    response_model_by_alias=False,
)
async def list_polygon_collection(request: Request, ):
    return PolygonCollection(polygons=await
                             request.app.state.polygons.find().to_list(1000))
