"""
Collects API calls related to withdrawal events.

A withdrawal resource used to indicate that product should be separated
(e.g. colostrum from newly lactating cows).

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.5.0 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.5.0/resources/icarWithdrawalEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Query, Request, Security, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id
from typing_extensions import Annotated

from ..ftCommon import add_one_to_db, dateBuild, delete_one_from_db, find_in_db
from ..icar.icarResources import icarWithdrawalEventResource as Withdrawal
from ..users import User, get_current_active_user

router = APIRouter(
    prefix="/withdrawal",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "Withdrawal"


class WithdrawalCollection(BaseModel):
    withdrawal: List[Withdrawal]


@router.post(
    "/",
    response_description="Add withdrawal event",
    response_model=Withdrawal,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_withdrawal_event(
    request: Request,
    withdrawal: Withdrawal,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_withdrawal"])
    ],
):
    """
    Create a new withdrawal event.

    :param withdrawal: Withdrawal to be added
    """
    return await add_one_to_db(
        withdrawal, request.app.state.withdrawal, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a withdrawal event")
async def remove_withdrawal_event(
    request: Request,
    ft: mongo_object_id.MongoObjectId,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["write_withdrawal"])
    ],
):
    """
    Delete a withdrawal event.

    :param ft: ObjectID of the withdrawal event to delete
    """
    return await delete_one_from_db(
        request.app.state.withdrawal, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for withdrawal event",
    response_model=WithdrawalCollection,
    response_model_by_alias=False,
)
async def withdrawal_event_query(
    request: Request,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["read_withdrawal"])
    ],
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    endDateTimeStart: datetime | None = datetime(1970, 1, 1, 0, 0, 0),
    endDateTimeEnd: Annotated[
        datetime, Query(default_factory=datetime.now)
    ] = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
    source: str | None = None,
    sourceId: str | None = None,
):
    """Search for a withdrawal event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "endDateTime": dateBuild(endDateTimeStart, endDateTimeEnd),
        "meta.created": dateBuild(createdStart, createdEnd),
        "meta.source": source,
        "meta.sourceId": sourceId,
    }
    result = await find_in_db(request.app.state.withdrawal, query)
    return WithdrawalCollection(withdrawal=result)
