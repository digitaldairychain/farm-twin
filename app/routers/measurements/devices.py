"""
Collects API calls related to devices.

Devices are physical devices, deployed in the real world.

A device may have several sensors attached to it.

An on-farm example is an outdoor weather station.

This collection of endpoints allows for the addition, update, deletion
and finding of those devices.

Compliant with ICAR data standards:
https://github.com/adewg/ICAR/blob/ADE-1/resources/icarDeviceResource.json
"""

import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request, Query
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing import Optional, List, Annotated
from bson.objectid import ObjectId
from ..icar import icarEnums, icarTypes
from datetime import datetime
from ..ftCommon import FTModel, filterQuery

router = APIRouter(
    prefix="/devices",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


class Device(FTModel):
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier on location level in the source"
            + " system for this device.",
        }
    )

    serial: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Optionally, the serial number of the device.",
            "example": "12345",
        },
    )

    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name given to the device by the farmer.",
        },
    )

    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Description of the device by the farmer.",
        },
    )
    softwareVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Version of the software installed on the device.",
        },
    )

    hardwareVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Version of the hardware installed in the device.",
        },
    )

    isActive: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicates whether the device is active at "
            + "this moment.",
        },
    )

    supportedMessages: Optional[List[icarEnums.icarMessageType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies message types supported for the device",
        },
    )

    manufacturer: Optional[icarTypes.icarDeviceManufacturerType] = Field(
        default=None,
        json_schema_extra={
            "description": "The device data as defined by the manufacturer.",
        },
    )

    registration: Optional[icarTypes.icarDeviceRegistrationIdentifierType] = (
        Field(
            default=None,
            json_schema_extra={
                "description": " registration identifier for the device "
                + "(most devices should eventually have a registration "
                + "issued by `org.icar` or other entity",
            },
        )
    )


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
            device.model_dump(by_alias=True, exclude=["ft"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Device already exists")
    if (
        created_device := await request.app.state.devices.find_one(
            {"_id": new_device.inserted_id}
        )
    ) is not None:
        return created_device
    raise HTTPException(
        status_code=404, detail="Device not successfully added"
    )


@router.patch(
    "/{ft}",
    response_description="Update a device",
    response_model=Device,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_device(request: Request, ft: str, device: Device):
    """
    Update an existing device if it exists.

    :param id: ObjectID of the device to update
    :param device: Device to update this device with
    """
    await request.app.state.devices.update_one(
        {"_id": ObjectId(ft)},
        {"$set": device.model_dump(by_alias=True, exclude=["ft", "created"])},
        upsert=False,
    )
    if (
        updated_device := await request.app.state.devices.find_one(
            {"_id": ObjectId(ft)}
        )
    ) is not None:
        return updated_device
    raise HTTPException(
        status_code=404, detail=f"Device {id} not successfully updated"
    )


@router.delete("/{ft}", response_description="Delete a device")
async def remove_device(request: Request, ft: str):
    """
    Delete a device.

    :param ft: ObjectID of the device to delete
    """
    delete_result = await request.app.state.devices.delete_one(
        {"_id": ObjectId(ft)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Device {ft} not found")


@router.get(
    "/",
    response_description="Search for devices",
    response_model=DeviceCollection,
    response_model_by_alias=False,
)
async def device_query(
    request: Request,
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
    createdStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    createdEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None,
    modifiedStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    modifiedEnd: Annotated[datetime, Query(
        default_factory=datetime.now)] = None
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
        "created": {"$gte": createdStart, "$lte": createdEnd},
        "modified": {"$gte": modifiedStart, "$lte": modifiedEnd}
    }
    result = await request.app.state.devices.find(
        filterQuery(query)).to_list(1000)
    if len(result) > 0:
        return DeviceCollection(devices=result)
    raise HTTPException(status_code=404, detail="No match found")
