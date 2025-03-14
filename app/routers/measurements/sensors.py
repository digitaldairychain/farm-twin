"""
Collects API calls related to sensors.

Sensors are instruments which measure a specific attribute.

A sensor will produce multiple samples over its lifetime.

A device can have several sensors.

An on-farm example is a temperature sensor.

This collection of endpoints allows for the addition, deletion
and finding of those sensors.
"""
import uuid

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
    id: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            'description': 'UUID of sensor',
            'example': str(uuid.uuid4())}
    )
    device: PyObjectId = Field(json_schema_extra={
        'description': 'UUID of device to which the sensor is connected',
        'example': str(uuid.uuid4())})
    tag: Optional[str] = Field(json_schema_extra={
        'description': 'ID tag or label on sensor',
        'example': '12345'})
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
    """
    Delete a sensor.

    :param sensor: UUID of the sensor to delete
    """
    delete_result = await request.app.state.sensors.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Sensor {id} not found")


@router.get(
    "/",
    response_description="Search for sensors",
    response_model=SensorCollection,
    response_model_by_alias=False,
)
async def sensor_query(request: Request,
                       id: str | None = None,
                       device: str | None = None,
                       tag: str | None = None,
                       measurement: str | None = None):
    """
    Search for a sensor given the provided criteria.

    :param id: Object ID of the sensor
    :param device: Object ID of the device to which the sensor(s) are attached
    :param tag: Tag of the sensor(s)
    :param measurement: Measurement type of the sensor(s)
    """
    query = {
        "_id": id,
        "device": device,
        "tag": tag,
        "measurement": measurement}
    filtered_query = {k: v for k, v in query.items() if v is not None}
    if (
        result := await request.app.state.sensors.find(filtered_query)
        .to_list(1000)
    ) is not None:
        return SensorCollection(sensors=result)
    raise HTTPException(status_code=404, detail="No match found")
