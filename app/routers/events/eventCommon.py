from ..ftCommon import FTModel
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import Field
from bson.objectid import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]


class AnimalEventModel(FTModel):
    """farm-twin common model parameters."""
    animal: PyObjectId = Field(
        json_schema_extra={
            "description": "ObjectID of animal.",
            "example": str(ObjectId()),
        }
    )
