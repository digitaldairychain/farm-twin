"""
Collects API calls related to attachments.

An attachment is a physical linkage between a measurement device and a thing.

A thing may have several devices attached to it.

These attachments are temporal in that they can be permanently or temporarily
attached.

An on-farm example is a soil measurement device attached to a stake in a field.

This collection of endpoints allows for the addition, deletion
and finding of those attachments.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from .ftCommon import add_one_to_db, delete_one_from_db, find_in_db
from .users import User, get_current_active_user

router = APIRouter(
    prefix="/attachments",
    tags=["attachments"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Attachment"


class Attachment(BaseModel):
    id: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id", default=None
    )
    device: mongo_object_id.MongoObjectId
    thing: mongo_object_id.MongoObjectId
    start: Optional[datetime] = Field(default=datetime.now())
    end: Optional[datetime] = Field(default=None)


class AttachmentCollection(BaseModel):
    attachments: List[Attachment]


@router.post(
    "/",
    response_description="Add new attachment",
    response_model=Attachment,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_attachment(
    request: Request,
    attachment: Attachment,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_attachments"])
    ],
):
    return await add_one_to_db(
        attachment, request.app.state.attachments, ERROR_MSG_OBJECT
    )


@router.delete("/{id}", response_description="Delete an attachment")
async def remove_attachment(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_attachments"])
    ],
):
    return await delete_one_from_db(
        request.app.state.attachments, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for attachments",
    response_model=AttachmentCollection,
    response_model_by_alias=False,
)
async def attachment_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_attachments"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    device: mongo_object_id.MongoObjectId | None = None,
    thing: mongo_object_id.MongoObjectId | None = None,
):
    query = {
        "_id": ft,
        "device": device,
        "thing": thing,
    }
    result = await find_in_db(request.app.state.attachments, query)
    return AttachmentCollection(attachments=result)
