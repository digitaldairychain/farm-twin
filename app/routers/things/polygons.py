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
import uuid

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from geojson_pydantic import MultiPolygon, FeatureCollection
from bson.objectid import ObjectId


router = APIRouter(
    prefix="/polygons",
    tags=["things"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Polygon(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, json_schema_extra={
        'description': 'UUID of polygon',
        'example': str(uuid.uuid4())})
    polygon: MultiPolygon = Field(json_schema_extra={
        'description': 'GeoJSON MultiPolygon, used to describe an enclosure or space, such as an animal pen'})
    tags: Optional[List[str]] = Field(default=[])


@router.post(
    "/",
    response_description="Add new polygon",
    response_model=Polygon,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_polygon(request: Request, polygon: Polygon):
    """
    Create a new polygon.

    :param polygon: Polygon to be added
    """
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
    """
    Delete a polygon.

    :param id: UUID of the polygon to delete
    """
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
    """
    Fetch a single polygon.

    :param id: UUID of the polygon to fetch details of
    """
    if (
        polygon := await request.app.state.polygons.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return polygon

    raise HTTPException(status_code=404, detail=f"Polygon {id} not found")


@router.get(
    "/",
    response_description="List all polygons",
    response_model=FeatureCollection,
    response_model_by_alias=False,
)
async def list_polygon_collection(request: Request, response: Response):
    """Fetch all current polygons."""
    fc = {"type": "FeatureCollection", "features": []}
    polygons = await request.app.state.polygons.find().to_list(1000)
    for polygon in polygons:
        f = {
             "type": "Feature",
             "properties": {
                 "objectid": str(polygon["_id"])
             },
             "geometry": polygon["polygon"]
        }
        fc["features"].append(f)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return fc
