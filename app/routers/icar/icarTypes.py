"""
Collection of types used in ICAR data standards.

See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/types
"""
from typing import List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pydantic_extra_types import mongo_object_id

from . import icarEnums


class icarIndividualWeightType(BaseModel):
    animal: mongo_object_id.MongoObjectId
    weight: float


class icarIdentifierType(BaseModel):
    id: str
    scheme: str


class icarMetricType(icarIdentifierType):
    pass


class icarStatisticType(BaseModel):
    metric: icarMetricType
    unit: str
    aggregation: icarEnums.icarAggregationType
    value: float


class icarMassMeasureType(BaseModel):
    measurement: float = Field(
        ge=0,
        json_schema_extra={
            'description': 'The weight observation, in the units specified (usually kilograms).',
        }
    )
    units: icarEnums.uncefactMassUnitsType = Field(
        default="KGM",
        json_schema_extra={
            'description': 'Units specified in UN/CEFACT 3-letter form.',
        }
    )
    method: icarEnums.icarWeightMethodType = Field(
        default='LoadCell',
        json_schema_extra={
            'description': 'The method of observation. Loadcell is the default if not specified.'
        }
    )
    resolution: Optional[float] = Field(
        default=None,
        json_schema_extra={
            'description': 'The smallest measurement difference that can be '
            + 'discriminated given the current device settings.',
            'example': 0.5
        }
    )


class Fractions(BaseModel):
    breed: str
    fraction: float


class icarBreedFractions(BaseModel):
    denominator: int
    fractions: List[Fractions]


class icarDeviceManufacturerType(BaseModel):
    id: str = Field(
        default=None,
        json_schema_extra={
            'description': 'Unique id of the manufacturer. Domain name/url --> lely.com, …',
        }
    )
    deviceType: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'A device type registered within the database proposed by the Sensor Working Group. This could be a UUID but we prefer a meaningful string.',
        }
    )
    deviceName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'Name given to the device by the manufacturer.',
        }
    )
    deviceDescription: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'Description of the device by the manufacturer.'
        }
    )
    deviceConfiguration: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'Configuration of the device.'
        }
    )


class icarDeviceRegistrationIdentifierType(icarIdentifierType):
    pass


class icarFeedDurationType(BaseModel):
    unitCode: icarEnums.uncefactTimeUnitsType = Field(
        json_schema_extra={
            'description': 'UN/CEFACT Common Code for Units of Measurement.',
            'example': 'MIN'
        }
    )
    value: float = Field(
        json_schema_extra={
            'description': 'The duration of the feeding in the units ' +
            'specified.'
        }
    )


class icarFeedQuantityType(BaseModel):
    unitCode: icarEnums.uncefactMassUnitsType = Field(
        default="KGM",
        json_schema_extra={
            'description': 'Units specified in UN/CEFACT 3-letter form.',
            'example': 'KGMs'
        }
    )
    value: float = Field(
        json_schema_extra={
            'description': 'The feed quantity in the units specified.'
        }
    )


class icarCostType(BaseModel):
    currency: str = Field(
        json_schema_extra={
            'description': 'The currency of the cost expressed using the ' +
            'ISO 4217 3-character code (such as AUD, GBP, USD, EUR).',
            'example': 'USD'
        }
    )
    value: float = Field(
        json_schema_extra={
            'description': 'The costs in the units specified.'
        }
    )


class NutritionModel(BaseModel):
    entitlement: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            'description': 'The amount of feed the animal/group was ' +
            'entitled to receive'
        }
    )
    delivered: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            'description': 'The amount of feed the animal/group received. ' +
            'If not present, it can be assumed that the delivered will be ' +
            'equal to entitlement'
        }
    )
    feedConsumption: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            'description': 'The amount of feed the animal/group has consumed'
        }
    )
    dryMatterPercentage: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'description': 'The dry matter content of the ration provided or ' +
            'consumed, expressed as a percentage.'
        }
    )
    totalCost: Optional[icarCostType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Total cost applied to this feeding. Based on ' +
            'the delivered or entitled amount'
        }
    )


class icarConsumedFeedType(NutritionModel):
    feedID: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID the feed consumed",
            "example": str(ObjectId()),
        }
    )


class icarConsumedRationType(NutritionModel):
    rationID: mongo_object_id.MongoObjectId = Field(
        json_schema_extra={
            "description": "ObjectID the ration consumed",
            "example": str(ObjectId()),
        }
    )
