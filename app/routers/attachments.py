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

import pymongo
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

router = APIRouter(
    prefix="/attachments",
    tags=["attachments"],
    responses={404: {"description": "Not found"}},
)


class Attachment(BaseModel):
    id: Optional[mongo_object_id.MongoObjectId] = Field(
        alias="_id", default=None)
    device: str
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
async def create_attachment(request: Request, attachment: Attachment):
    try:
        new_attachment = await request.app.state.attachments.insert_one(
            attachment.model_dump(by_alias=True, exclude=["id"])
        )
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Attachment {attachment.coordinate}" + " already exists",
        )
    if (
        created_attachment := await request.app.state.attachments.find_one(
            {"_id": new_attachment.inserted_id}
        )
    ) is not None:
        return created_attachment
    raise HTTPException(
        status_code=404,
        detail="Attachment " + f"{attachment._id} not successfully added",
    )


@router.delete("/{id}", response_description="Delete an attachment")
async def remove_attachment(request: Request, id: str):
    delete_result = await request.app.state.attachments.delete_one(
        {"_id": ObjectId(id)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Attachment {id} not found")


@router.get(
    "/",
    response_description="Search for attachments",
    response_model=AttachmentCollection,
    response_model_by_alias=False,
)
async def attachment_query(
    request: Request,
    id: str | None = None,
    device: str | None = None,
    object: str | None = None,
):
    query = {"_id": id, "object": object, "device": device}
    filtered_query = {k: v for k, v in query.items() if v is not None}
    if (
        result := await request.app.state.attachments.find(filtered_query).to_list(1000)
    ) is not None:
        return AttachmentCollection(attachments=result)
    raise HTTPException(status_code=404, detail="No match found")
