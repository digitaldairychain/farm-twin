from ..ftCommon import FTModel

from pydantic_extra_types import mongo_object_id
from pydantic import Field
from bson.objectid import ObjectId


class AnimalEventModel(FTModel):
    """farm-twin common model parameters."""
    animal: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of animal.",
            "example": str(ObjectId()),
        }
    )
