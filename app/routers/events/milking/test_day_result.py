"""
Collects API calls related to an animal being dried off at the end of a lactation.

This collection of endpoints allows for the addition, deletion
and finding of those events.

Compliant with v1.4.1 ICAR Animal Data Exchange standards:
https://github.com/adewg/ICAR/blob/v1.4.1/resources/icarTestDayResultEventResource.json
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from pydantic_extra_types import mongo_object_id

from ...ftCommon import (add_one_to_db, dateBuild, delete_one_from_db,
                         find_in_db)
from ...icar import icarEnums
from ...icar.icarResources import \
    icarTestDayResultEventResource as TestDayResult

ERROR_MSG_OBJECT = "Test Day Result"

router = APIRouter(
    prefix="/test_day_result",
    tags=["milking"],
    responses={404: {"description": "Not found"}},
)


class TestDayResultCollection(BaseModel):
    test_day_result: List[TestDayResult]


@router.post(
    "/",
    response_description="Add test day result event",
    response_model=TestDayResult,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_test_day_result_event(
    request: Request, test_day_result: TestDayResult
):
    """
    Create a new test day result event.

    :param test_day_result: Test day result to be added
    """
    return await add_one_to_db(
        test_day_result, request.app.state.test_day_result, ERROR_MSG_OBJECT
    )


@router.delete("/{ft}", response_description="Delete a test day result event")
async def remove_test_day_result_event(
    request: Request, ft: mongo_object_id.MongoObjectId
):
    """
    Delete a test day result event.

    :param ft: ObjectID of the test day result event to delete
    """
    return await delete_one_from_db(
        request.app.state.test_day_result, ft, ERROR_MSG_OBJECT
    )


@router.get(
    "/",
    response_description="Search for test day result event",
    response_model=TestDayResultCollection,
    response_model_by_alias=False,
)
async def test_day_result_event_query(
    request: Request,
    ft: mongo_object_id.MongoObjectId | None = None,
    animal: str | None = None,
    testDayCode: icarEnums.icarTestDayCodeType | None = None,
    createdStart: datetime | None = None,
    createdEnd: datetime | None = None,
):
    """Search for a test day result event given the provided criteria."""
    query = {
        "_id": ft,
        "animal.id": animal,
        "testDayCode": testDayCode,
        "created": dateBuild(createdStart, createdEnd),
    }
    result = await find_in_db(request.app.state.test_day_result, query)
    return TestDayResultCollection(test_day_result=result)
