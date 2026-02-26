"""
Collects API calls related to imagery.

This collection of endpoints allows for the uploading, deletion
and downloading of those images.
"""

import io
from datetime import datetime
from typing import List

import gridfs
from bson.objectid import ObjectId
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Request,
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
    update_one_in_db,
)
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/image",
    tags=["imagery"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Image"


@router.post(
    "/",
    response_description="Upload new image",
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    request: Request,
    file: UploadFile,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_imagery"])
    ],
):
    """
    Upload a new image.

    :param file: Image file  to be uploaded
    """
    bucket = gridfs.AsyncGridFSBucket(request.app.state.images)
    async with bucket.open_upload_stream(
        file.filename, metadata={"contentType": file.content_type}
    ) as grid_in:
        await grid_in.write(file)
    return {"ft": str(grid_in._id)}


@router.delete("/{ft}", response_description="Delete an image")
async def remove_image(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_imagery"])
    ],
):
    """
    Delete an image file.

    :param id: UUID of the image to delete
    """
    try:
        bucket = gridfs.AsyncGridFSBucket(request.app.state.images)
        await bucket.delete(ObjectId(ft))
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail=f"Image {ft} not found")


@router.get(
    "/",
    response_description="Download an image",
    response_class=StreamingResponse,
)
async def image_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_imagery"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
):
    """
    Download an image given the provided criteria.
    """
    bucket = gridfs.AsyncGridFSBucket(request.app.state.images)
    try:
        file = await bucket.open_download_stream(ObjectId(ft))
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail=f"Image {ft} not found")
    contents = await file.read()
    return StreamingResponse(
        io.BytesIO(contents),
        media_type=file.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={file.filename}"
        },
    )
