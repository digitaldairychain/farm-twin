"""
Collection of types used in ICAR data standards.

See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/types
"""
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from typing import List, Optional
from . import icarEnums

PyObjectId = Annotated[str, BeforeValidator(str)]


class icarIndividualWeightType(BaseModel):
    animal: PyObjectId
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
