"""
Collects API calls related to devices.

Devices are physical devices, deployed in the real world.

A device may have several sensors attached to it.

An on-farm example is an outdoor weather station.

This collection of endpoints allows for the addition, update, deletion
and finding of those devices.
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/devices",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Device(BaseModel):
    id: Optional[PyObjectId] = Field(
        alias="_id",
        default=None,
        json_schema_extra={
            'description': 'ObjectID of device',
            'example': str(ObjectId())}
    )
    tag: str = Field(json_schema_extra={
        'description': 'ID tag or label on device',
        'example': '12345'})
    vendor: str = Field(json_schema_extra={
        'description': 'Manufacturer of device',
        'example': 'Acme Sensor Co.'})
    model: str = Field(json_schema_extra={
        'description': 'Model number or designation of device',
        'example': 'Super Device 9000'})


class DeviceCollection(BaseModel):
    devices: List[Device]


@router.post(
    "/",
    response_description="Add new device",
    response_model=Device,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_device(request: Request, device: Device):
    """
    Create a new device if it does not already exist.

    :param device: Device to be added
    """
    try:
        new_device = await request.app.state.devices.insert_one(
            device.model_dump(by_alias=True, exclude=["id"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404,
                            detail="Device already exists")
    if (
        created_device := await
        request.app.state.devices.find_one({"_id": new_device.inserted_id})
    ) is not None:
        return created_device
    raise HTTPException(status_code=404,
                        detail="Device not successfully added")


@router.patch(
        "/{id}",
        response_description="Update a device",
        response_model=Device,
        status_code=status.HTTP_202_ACCEPTED
    )
async def update_device(request: Request, id: str, device: Device):
    """
    Update an existing device if it exists.

    :param id: ObjectID of the device to update
    :param device: Device to update this device with
    """
    await request.app.state.devices.update_one(
        {"_id": ObjectId(id)},
        {'$set': device.model_dump(by_alias=True, exclude=["id"])},
        upsert=False
    )

    if (
        updated_device := await
        request.app.state.devices.find_one({"_id": ObjectId(id)})
    ) is not None:
        return updated_device
    raise HTTPException(status_code=404,
                        detail=f"Device {id} not successfully updated")


@router.delete("/{id}", response_description="Delete a device")
async def remove_device(request: Request, id: str):
    """
    Delete a device.

    :param id: ObjectID of the device to delete
    """
    delete_result = await request.app.state.devices.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Device {id} not found")


@router.get(
    "/",
    response_description="Search for devices",
    response_model=DeviceCollection,
    response_model_by_alias=False,
)
async def device_query(request: Request,
                       id: str | None = None,
                       tag: str | None = None,
                       vendor: str | None = None,
                       model: str | None = None,):
    """
    Search for a device given the provided criteria.

    :param id: Object ID of the device
    :param tag: Tag of the device(s)
    :param vendor: Vendor of the device(s)
    :param model: Model designation of the device(s)
    """
    if id:
        id = ObjectId(id)
    query = {
        "_id": id,
        "tag": tag,
        "vendor": vendor,
        "model": model}
    filtered_query = {k: v for k, v in query.items() if v is not None}
    result = await request.app.state.devices.find(filtered_query).to_list(1000)
    if len(result) > 0:
        return DeviceCollection(devices=result)
    raise HTTPException(status_code=404, detail="No match found")
