"""
Collects API calls related to animal feed intake events.

The duration and consumption of feed by animals may be periodically recorded
across a farm.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarFeedIntakeEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ...ftCommon import (
    add_one_to_db,
    dateBuild,
    delete_one_from_db,
    find_in_db,
)
from ...icar.icarResources import icarFeedIntakeEventResource as FeedIntake
from ...users import User, get_current_active_user

router = APIRouter(
    prefix="/feed_intake",
    tags=["feeding"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Feed Intake"


class FeedIntakeCollection(BaseModel):
    feed_intake: List[FeedIntake]


@router.post(
    "/",
    response_description="Add feedintake event",
    response_model=FeedIntake,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_feed_intake_event(
    request: Request,
    feed_intake: FeedIntake,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_feeding"])
    ],
):
    """
    Create a new feed intake event.

    :param feedintake: Feed intake to be added
    """
    return await add_one_to_db(
        feed_intake, request.app.state.feed_intake, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a feed intake event")
async def remove_feed_intake_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_feeding"])
    ],
):
    """
    Delete a feed intake event.

    :param ft: ObjectID of the feed intake event to delete
    """
    return await delete_one_from_db(
        request.app.state.feed_intake, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for feed intake event",
    response_model=FeedIntakeCollection,
    response_model_by_alias=False,
)
async def feed_intake_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_feeding"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    device: str | None = None,
    feedingStartingDateTimeStart: datetime | None = None,
    feedingStartingDateTimeEnd: datetime | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a feed intake event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "device.id": device,
        "feedingStartingDateTime": dateBuild(
            feedingStartingDateTimeStart, feedingStartingDateTimeEnd
        ),
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.feed_intake, query)
    return FeedIntakeCollection(feed_intake=result)
