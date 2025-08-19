"""
Collects API calls related to sensors.

Sensors are instruments which measure a specific attribute.

A sensor will produce multiple samples over its lifetime.

A device can have several sensors.

An on-farm example is a temperature sensor.

This collection of endpoints allows for the addition, deletion
and finding of those sensors.
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import FTModel, dateBuild, filterQuery

router = APIRouter(
    prefix="/sensors",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


class Sensor(FTModel):
    device: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "UUID of device to which the sensor is connected",
            "example": str(ObjectId()),
        }
    )
    serial: Optional[str] = Field(
        default="",
        json_schema_extra={
            "description": "Serial or label on sensor",
            "example": "12345",
        },
    )
    measurement: str = Field(
        json_schema_extra={
            "description": "Description or type of measurement",
            "example": "Soil Temperature",
        }
    )


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
    try:
        new_sensor = await request.app.state.sensors.insert_one(
            sensor.model_dump(by_alias=True, exclude=["ft", "resourceType"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Sensor already exists")
    if (
        created_sensor := await request.app.state.sensors.find_one(
            {"_id": new_sensor.inserted_id}
        )
    ) is not None:
        return created_sensor
    raise HTTPException(
        status_code=404, detail=f"Sensor {new_sensor.ft} not " + "successfully added"
    )


@router.patch(
    "/{ft}",
    response_description="Update a sensor",
    response_model=Sensor,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_sensor(request: Request, ft: str, sensor: Sensor):
    """
    Update an existing sensor if it exists.

    :param ft: ObjectID of the sensor to update
    :param sensor: Sensor to update this sensor with
    """
    await request.app.state.sensors.update_one(
        {"_id": ObjectId(ft)},
        {"$set": sensor.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False,
    )

    if (
        updated_sensor := await request.app.state.sensors.find_one(
            {"_id": ObjectId(ft)}
        )
    ) is not None:
        return updated_sensor
    raise HTTPException(status_code=404, detail=f"Sensor {id} not successfully updated")


@router.delete("/{ft}", response_description="Delete a sensor")
async def remove_sensor(request: Request, ft: str):
    """
    Delete a sensor.

    :param ft: ObjectID of the sensor to delete
    """
    delete_result = await request.app.state.sensors.delete_one({"_id": ObjectId(ft)})

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
    ft: mongo_object_id.MongoObjectId | None = None,
    device: mongo_object_id.MongoObjectId | None = None,
    serial: str | None = None,
    measurement: str | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
):
    """Search for a sensor given the provided criteria."""
    query = {
        "_id": ft,
        "device": device,
        "serial": serial,
        "measurement": measurement,
        "created": dateBuild(createdStart, createdEnd),
        "modified": dateBuild(modifiedStart, modifiedEnd),
    }
    result = await request.app.state.sensors.find(filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return SensorCollection(sensors=result)
    raise HTTPException(status_code=404, detail="No match found")
