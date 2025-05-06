"""
Collects API calls related to sensors.

Sensors are instruments which measure a specific attribute.

A sensor will produce multiple samples over its lifetime.

A device can have several sensors.

An on-farm example is a temperature sensor.

This collection of endpoints allows for the addition, deletion
and finding of those sensors.
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId
from ..ftCommon import FTModel, modifiedFilter
from datetime import datetime

router = APIRouter(
    prefix="/sensors",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Sensor(FTModel):
    device: PyObjectId = Field(json_schema_extra={
        'description': 'UUID of device to which the sensor is connected',
        'example': str(ObjectId())})
    serial: Optional[str] = Field(
        default='',
        json_schema_extra={
            'description': 'Serial or label on sensor',
            'example': '12345'}
    )
    measurement: str = Field(json_schema_extra={
        'description': 'Description or type of measurement',
        'example': 'Soil Temperature'})


class SensorCollection(BaseModel):
    sensors: List[Sensor]


@router.post(
    "/",
    response_description="Add new sensor",
    response_model=Sensor,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_sensor(request: Request, sensor: Sensor):
    """
    Create a new sensor.

    :param sensor: Sensor to be added.
    """
    sensor.created = datetime.now()
    try:
        new_sensor = await request.app.state.sensors.insert_one(
            sensor.model_dump(by_alias=True, exclude=["ft", "modified"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail="Sensor already exists")
    if (
        created_sensor := await
        request.app.state.sensors.find_one({"_id": new_sensor.inserted_id})
    ) is not None:
        return created_sensor
    raise HTTPException(status_code=404,
                        detail=f"Sensor {new_sensor.ft} not successfully added")


@router.patch(
        "/{ft}",
        response_description="Update a sensor",
        response_model=Sensor,
        status_code=status.HTTP_202_ACCEPTED
    )
async def update_sensor(request: Request, ft: str, sensor: Sensor):
    """
    Update an existing sensor if it exists.

    :param ft: ObjectID of the sensor to update
    :param sensor: Sensor to update this sensor with
    """
    await request.app.state.sensors.update_one(
        {"_id": ObjectId(ft)},
        {'$set': sensor.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False
    )

    if (
        updated_sensor := await
        request.app.state.sensors.find_one({"_id": ObjectId(ft)})
    ) is not None:
        return updated_sensor
    raise HTTPException(status_code=404,
                        detail=f"Sensor {id} not successfully updated")


@router.delete("/{ft}", response_description="Delete a sensor")
async def remove_sensor(request: Request, ft: str):
    """
    Delete a sensor.

    :param ft: ObjectID of the sensor to delete
    """
    delete_result = await request.app.state.sensors.delete_one(
        {"_id": ObjectId(ft)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sensor {ft} not found")


@router.get(
    "/",
    response_description="Search for sensors",
    response_model=SensorCollection,
    response_model_by_alias=False,
)
async def sensor_query(
                       request: Request,
                       ft: str | None = None,
                       device: str | None = None,
                       serial: str | None = None,
                       measurement: str | None = None,
                       createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
                       createdEnd: datetime | None = None,
                       modifiedStart: datetime | None = None,
                       modifiedEnd: datetime | None = None,):
    """Search for a sensor given the provided criteria."""
    if ft:
        ft = ObjectId(ft)
    if not createdEnd:
        createdEnd = datetime.now()
    mod = modifiedFilter(modifiedStart, modifiedEnd)
    query = {
        "_id": ft,
        "device": device,
        "serial": serial,
        "measurement": measurement}
    filtered_query = {k: v for k, v in query.items() if v is not None}
    filtered_query["created"] = {"$gte": createdStart, "$lte": createdEnd}
    if mod.search:
        filtered_query["modified"] = {"$gte": mod.start, "$lte": mod.end}
    result = await request.app.state.sensors.find(filtered_query).to_list(1000)
    if len(result) > 0:
        return SensorCollection(sensors=result)
    raise HTTPException(status_code=404, detail="No match found")
