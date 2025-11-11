"""
Collects API calls related to devices.

Devices are physical devices, deployed in the real world.

A device may have several sensors attached to it.

An on-farm example is an outdoor weather station.

This collection of endpoints allows for the addition, update, deletion
and finding of those devices.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarDeviceResource.json
"""

from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Query, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ..ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
    update_one_in_db,
)
from ..icar import icarTypes
from ..icar.icarResources import icarDeviceResource as Device
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/devices",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Device"


class DeviceCollection(BaseModel):
    devices: List[Device]


@router.post(
    "/",
    response_description="Add new device",
    response_model=Device,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_device(
    request: Request,
    device: Device,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_devices"])
    ],
):
    """
    Create a new device if it does not already exist.

    :param device: Device to be added
    """
    return await add_one_to_db(
        device, request.app.state.devices, ERROR_MSG_OBJECT
    )


@router.patch(
    "/{ft}",
    response_description="Update a device",
    response_model=Device,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_device(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    device: Device,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_devices"])
    ],
):
    """
    Update an existing device if it exists.

    :param id: ObjectID of the device to update
    :param device: Device to update this device with
    """
    return await update_one_in_db(
        device, request.app.state.devices, ft, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a device")
async def remove_device(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_devices"])
    ],
):
    """
    Delete a device.

    :param ft: ObjectID of the device to delete
    """
    return await delete_one_from_db(
        request.app.state.devices, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for devices",
    response_model=DeviceCollection,
    response_model_by_alias=False,
)
async def device_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_devices"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    id: str | None = None,
    serial: str | None = None,
    name: str | None = None,
    description: str | None = None,
    softwareVersion: str | None = None,
    hardwareVersion: str | None = None,
    isActive: bool | None = None,
    supportedMessages: Annotated[list[str] | None, Query()] = [],
    manufacturer: icarTypes.icarDeviceManufacturerType | None = None,
    registration: icarTypes.icarDeviceRegistrationIdentifierType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    modifiedStart: datetime | None = None,
    modifiedEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a device given the provided criteria."""
    query = {
        "_id": ft,
        "id": id,
        "serial": serial,
        "name": name,
        "description": description,
        "softwareVersion": softwareVersion,
        "hardwareVersion": hardwareVersion,
        "isActive": isActive,
        "manufacturer": manufacturer,
        "registration": registration,
        "supportedMessages": {"$in": supportedMessages},
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.modified": dateBuild(modifiedStart, modifiedEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.devices, query)
    return DeviceCollection(devices=result)
