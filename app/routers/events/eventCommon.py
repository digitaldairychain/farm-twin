from bson.objectid import ObjectId
from pydantic import Field
from pydantic_extra_types import mongo_object_id

from ..ftCommon import FTModel


class AnimalEventModel(FTModel):
    """farm-twin common model parameters."""

    animal: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of animal.",
            "example": str(ObjectId()),
        }
    )
