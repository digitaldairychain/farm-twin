import pymongo

from fastapi import status, HTTPException, Response, APIRouter, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/attachments",
    tags=["attachments"],
    responses={404: {"description": "Not found"}},
)


PyObjectId = Annotated[str, BeforeValidator(str)]


class Attachment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    device: str
    thing: PyObjectId
    start:  Optional[datetime] = Field(default=datetime.now())
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
        raise HTTPException(status_code=404,
                            detail=f"Attachment {attachment.coordinate}" +
                            " already exists")
    if (
        created_attachment := await
        request.app.state.attachments.find_one(
            {"_id": new_attachment.inserted_id})
    ) is not None:
        return created_attachment
    raise HTTPException(status_code=404, detail="Attachment " +
                        f"{attachment._id} not successfully added")


@router.delete("/{id}", response_description="Delete a attachment")
async def remove_attachment(request: Request, id: str):
    delete_result = await request.app.state.attachments.delete_one(
        {"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Attachment {id} not found")


@router.get(
    "/{id}",
    response_description="Get a single attachment",
    response_model=Attachment,
    response_model_by_alias=False,
)
async def list_attachment_single(request: Request, id: str):
    if (
        attachment := await request.app.state.attachments.find_one(
            {"_id": ObjectId(id)})
    ) is not None:
        return attachment

    raise HTTPException(status_code=404, detail=f"Attachment {id} not found")


@router.get(
    "/",
    response_description="List all attachments",
    response_model=AttachmentCollection,
    response_model_by_alias=False,
)
async def list_attachment_collection(request: Request):
    return AttachmentCollection(attachments=await
                                request.app.state.attachments.find()
                                .to_list(1000))
