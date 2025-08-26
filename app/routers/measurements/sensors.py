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

from bson.objectid import ObjectId
from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (FTModel, add_one_to_db, dateBuild, delete_one_from_db,
                        find_in_db, update_one_in_db)

router = APIRouter(
    prefix="/sensors",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Sensor"


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
    return await add_one_to_db(sensor, request.app.state.sensors, ERROR_MSG_OBJECT)


@router.patch(
    "/{ft}",
    response_description="Update a sensor",
    response_model=Sensor,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_sensor(
    request: Request, ft: mongo_object_id.MongoObjectId, sensor: Sensor
):
    """
    Update an existing sensor if it exists.

    :param ft: ObjectID of the sensor to update
    :param sensor: Sensor to update this sensor with
    """
    return await update_one_in_db(
        sensor, request.app.state.sensors, ft, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a sensor")
async def remove_sensor(request: Request, ft: mongo_object_id.MongoObjectId):
    """
    Delete a sensor.

    :param ft: ObjectID of the sensor to delete
    """
    return await delete_one_from_db(request.app.state.sensors, ft, ERROR_MSG_OBJECT)


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
    result = await find_in_db(request.app.state.sensors, query)
    return SensorCollection(sensors=result)
