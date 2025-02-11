"""Sensor API

Sensors are instruments which measure a specific attribute.

A sensor will produce multiple samples over its lifetime.

A device can have several sensors.

This collection of endpoints allows for the addition, deletion
and finding of those sensors.
"""
from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/sensors",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Sensor(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    device: PyObjectId
    measurement: str
    serial: Optional[str] = Field(default=None)


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
    new_sensor = await request.app.state.sensors.insert_one(
        sensor.model_dump(by_alias=True, exclude=["id"])
    )

    if (
        created_sensor := await
        request.app.state.sensors.find_one({"_id": new_sensor.inserted_id})
    ) is not None:
        return created_sensor
    raise HTTPException(status_code=404,
                        detail=f"Sensor {id} not successfully added")


@router.patch(
        "/{id}",
        response_description="Update a sensor",
        response_model=Sensor,
        status_code=status.HTTP_202_ACCEPTED
    )
async def update_sensor(request: Request, id: str, sensor: Sensor):
    """
    Update an existing sensor if it exists.

    :param id: UUID of the sensor to update
    :param sensor: Sensor to update this sensor with
    """
    await request.app.state.sensors.update_one(
        {"_id": id},
        {'$set': sensor.model_dump(by_alias=True, exclude=["id"])},
        upsert=False
    )

    if (
        updated_sensor := await
        request.app.state.sensors.find_one({"tag": sensor.tag})
    ) is not None:
        return updated_sensor
    raise HTTPException(status_code=404,
                        detail=f"Sensor {sensor.tag} not successfully updated")


@router.delete("/{id}", response_description="Delete a sensor")
async def remove_sensor(request: Request, id: str):
    delete_result = await request.app.state.sensors.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sensor {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single sensor",
    response_model=Sensor,
    response_model_by_alias=False,
)
async def list_sensor_single(request: Request, id: str):
    """
    Delete a sensor.

    :param sensor: UUID of the sensor to delete
    """
    if (
        sensor := await request.app.state.sensors.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return sensor

    raise HTTPException(status_code=404, detail=f"Sensor {id} not found")


@router.get(
    "/",
    response_description="List all sensors",
    response_model=SensorCollection,
    response_model_by_alias=False,
)
async def list_sensor_collection(request: Request):
    """
    Fetch a single sensor given an ID.

    :param id: UUID of the sensor to fetch
    """
    return SensorCollection(sensors=await
                            request.app.state.sensors.find().to_list(1000))
