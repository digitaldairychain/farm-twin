"""
Collection of types used in ICAR data standards.

See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/types
"""
from datetime import datetime
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


class icarLocationIdentifierType(icarIdentifierType):
    pass


class icarDeclarationIdentifierType(icarIdentifierType):
    pass


class icarOrganizationIdentifierType(icarIdentifierType):
    pass


class postalAddress(BaseModel):
    addressCountry: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code.',
        }
    )
    addressLocality: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The locality in which the street address is, and which is in the region. For example, Mountain View.',
        }
    )
    addressRegion: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The region in which the locality is, and which is in the country. For example, California or another appropriate first-level Administrative division',
        }
    )
    postOfficeBoxNumber: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The post office box number for PO box addresses.',
        }
    )
    postalCode: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The postal code. For example, 94043.',
        }
    )
    streetAddress: str = Field(
        default=None,
        json_schema_extra={
            'description': 'The street address. For example, 1600 Amphitheatre Pkwy.',
        }
    )


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


class icarAnimalStateType(BaseModel):
    currentLactationParity: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'description': 'The current parity of the animal.'
        }
    )
    lastCalvingDate: Optional[datetime] = Field(
        default=None
    )
    lastInseminationDate: Optional[datetime] = Field(
        default=None
    )
    lastDryingOffDate: Optional[datetime] = Field(
        default=None
    )


class icarOrganizationIdentityType(BaseModel):
    name: str = Field(
        json_schema_extra={
            'description': 'Name of the organisation'
        }
    )
    leiCode: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'An organization identifier that uniquely identifies a legal entity as defined in ISO 17442.',
        }
    )
    globalLocationNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'The Global Location Number (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.',
        }
    )
    uri: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'A uniform resource identifier that is the unique reference or for this organisation, such as its web site.',
        }
    )


class icarOrganizationType(icarOrganizationIdentityType):
    establishmentIdentifiers: Optional[List[icarOrganizationIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            'description': 'Scheme and identifier combinations that provide official registrations for a business or establishment',
        }
    )
    address: Optional[postalAddress] = Field(
        default=None,
        json_schema_extra={
            'description': 'Postal address or physical address in postal format, including country. Optional as this may already be specified in a consignment.',
        }
    )
    parentOrganization: Optional[icarOrganizationIdentityType] = Field(
        default=None,
        json_schema_extra={
            'description': 'The larger organization that this organization is a sub-organization of, if any.',
        }
    )
    membershipIdentifiers: Optional[List[icarOrganizationIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            'description': 'Scheme and identifier combinations that identity membership in programmes',
        }
    )


class icarInterestedPartyType(icarOrganizationType):
    interests: List[str] = Field(
        json_schema_extra={
            'description': 'Identifies the type of interest that the party has in a consignment or animal.',
        }
    )


class icarConsignmentDeclarationType(BaseModel):
    declarationId: Optional[icarDeclarationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Identifies the specific declaration being made using a scheme and an id.',
        }
    )
    declaredValue: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'description': 'The value of the declaration.',
        }
    )


class icarConsignmentType(BaseModel):
    id: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'description': 'Official identifier for the movement.'
        }
    )
    id: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'Official identifier for the movement.'
        }
    )
    originLocation: Optional[icarLocationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'The location of the origin of the consignment expressed as a scheme and id.',
        }
    )
    originAddress: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'Origin address for movement.'
        }
    )
    originPostalAddress: Optional[postalAddress] = Field(
        default=None,
        json_schema_extra={
            'A structured, schema.org-style address for the origin location.',
        }
    )
    originOrganization: Optional[icarOrganizationType] = Field(
        default=None,
        json_schema_extra={
            'The organisational details of the origin, including any necessary identifiers.',
        }
    )
    destinationLocation: Optional[icarLocationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'The location of the destination of the consignment expressed as a scheme and id.',
        }
    )
    destinationAddress: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'Destination address for movement.'
        }
    )
    destinationPostalAddress: Optional[postalAddress] = Field(
        default=None,
        json_schema_extra={
            'A structured, schema.org-style address for the destination location.',
        }
    )
    destinationOrganization: Optional[icarOrganizationType] = Field(
        default=None,
        json_schema_extra={
            'The organisational details of the destination, including any necessary identifiers.',
        }
    )
    loadingDateTime: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            'RFC3339 UTC date and time animals were loaded for transport (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance).',
        }
    )
    unloadingDateTime: Optional[datetime] = Field(
        default=None,
        json_schema_extra={
            'RFC3339 UTC date and time animals were unloaded after transport (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance).',
        }
    )
    expectedDuration: Optional[float] = Field(
        default=None,
        json_schema_extra={
            'Expected duration of transportation in hours.'
        }
    )
    transportOperator: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'Transport operator official name (should really be schema.org/organization).',
        }
    )
    vehicle: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'Identification of the vehicle (for example, licence plate).'
        }
    )
    transportReference: Optional[str] = Field(
        default=None,
        json_schema_extra={
            'Shipping or transporter reference.'
        }
    )
    isolationFacilityUsed: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            'True if an isolation facility was used for the movement.'
        }
    )
    farmAssuranceReference: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            'Identification reference of a farm assurance operation.'
        }
    )
    countConsigned: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'The number of animals despatched or consigned from the origin.',
        }
    )
    countReceived: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'The number of animals received at the destination.'
        }
    )
    hoursOffFeed: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'The number of hours since animals in the consignment had access to feed.',
        }
    )
    hoursOffWater: Optional[int] = Field(
        default=None,
        json_schema_extra={
            'The number of hours since animals in the consignment had access to water.',
        }
    )
    references: Optional[List[icarIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            'References associated with the consignment. These may be additional to the single transport reference (for instance, to support multi-mode transport).',
        }
    )
    interestedParties: Optional[List[icarInterestedPartyType]] = Field(
        default=None,
        json_schema_extra={
            'Identifies the parties and their interests in the consignment.',
        }
    )
    declarations: Optional[List[icarConsignmentDeclarationType]] = Field(
        default=None,
        json_schema_extra={
            'Country, species or scheme -specific declarations for the consignment.',
        }
    )
