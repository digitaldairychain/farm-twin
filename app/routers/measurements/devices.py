"""Device API

Devices are physical devices, deployed in the real world.

A device may have several sensors attached to it.

This collection of endpoints allows for the addition, update, deletion
and finding of those devices.
"""
import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated

router = APIRouter(
    prefix="/devices",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Device(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    tag: str
    vendor: str
    model: str


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
                            detail=f"Device {device.tag} already exists")
    if (
        created_device := await
        request.app.state.devices.find_one({"_id": new_device.inserted_id})
    ) is not None:
        return created_device
    raise HTTPException(status_code=404,
                        detail=f"Device {device.tag} not successfully added")


@router.patch(
        "/{tag}",
        response_description="Update a device",
        response_model=Device,
        status_code=status.HTTP_202_ACCEPTED
    )
async def update_device(request: Request, tag: str, device: Device):
    """
    Update an existing device if it exists.

    :param tag: Tag of the device to update
    :param device: Device to update this device with
    """
    await request.app.state.devices.update_one(
        {"tag": tag},
        {'$set': device.model_dump(by_alias=True, exclude=["id"])},
        upsert=False
    )

    if (
        updated_device := await
        request.app.state.devices.find_one({"tag": device.tag})
    ) is not None:
        return updated_device
    raise HTTPException(status_code=404,
                        detail=f"Device {device.tag} not successfully updated")


@router.delete("/{tag}", response_description="Delete a device")
async def remove_device(request: Request, tag: str):
    """
    Delete a device.

    :param tag: Tag of the device to delete
    """
    delete_result = await request.app.state.devices.delete_one({"tag": tag})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Device {tag} not found")


@router.get(
    "/{tag}",
    response_description="Get a single device",
    response_model=Device,
    response_model_by_alias=False,
)
async def list_device_single(request: Request, tag: str):
    """
    Fetch a single device given a tag.

    :param tag: Tag of the device to fetch details of
    """
    if (
        device := await request.app.state.devices.find_one({"tag": tag})
    ) is not None:
        return device

    raise HTTPException(status_code=404, detail=f"Device {tag} not found")


@router.get(
    "/",
    response_description="List all devices",
    response_model=DeviceCollection,
    response_model_by_alias=False,
)
async def list_device_collection(request: Request):
    """Fetch all current devices."""
    return DeviceCollection(devices=await
                            request.app.state.devices.find().to_list(1000))
