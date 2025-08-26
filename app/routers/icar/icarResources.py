"""
Collection of types used in ICAR data standards.
See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/enums
"""

from typing import Optional

from pydantic import Field, FutureDatetime

from ..ftCommon import FTModel
from . import icarEnums, icarTypes


class icarSchemeTypeResource(FTModel):
    resourceType: str = Field(default_factory=lambda: icarSchemeTypeResource.__name__)
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Schema type/scheme name."},
    )


class icarResource(FTModel):
    resourceType: str = Field(
        json_schema_extra={
            "description": "Uniform resource identifier (URI) or shortname of the logical resourceType. The ResourceType catalog defines the set of allowed resourceTypes."
        },
    )
    self: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Uniform resource identifier (URI) of the resource (rel=self)."
        },
    )
    meta: icarTypes.icarMetaDataType = Field(
        default=None,
        json_schema_extra={
            "description": "Meta-data for the resource. Mandatory if you wish to support synchronisation. Systems should maintain and provide meta data if at all possible.ICAR ADE working group intend meta to be required in the next major release of ADE."
        },
    )
    location: Optional[icarTypes.icarLocationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique location scheme and identifier combination."
        },
    )


class icarReproEmbryoResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarReproEmbryoResource.__name__)
    id: Optional[icarTypes.icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Official identifier for the embryo (if any)."
        },
    )
    collectionCentre: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Identifies the collection centre."},
    )
    dateCollected: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC date of collection (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    donorIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "One or more unique scheme/identifier combinations for the donor dam."
        },
    )
    donorURI: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "URI to an AnimalCoreResource for the donor dam."
        },
    )
    sireIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "One or more unique scheme/identifier combinations for the sire."
        },
    )
    sireOfficialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name of the sire."},
    )
    sireURI: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "URI to an AnimalCoreResource for the sire."},
    )


class icarStatisticsResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarStatisticsResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier on location level in the source system for this statistics."
        },
    )
    location: icarTypes.icarLocationIdentifierType = Field(
        json_schema_extra={
            "description": "Unique location scheme and identifier combination."
        },
    )
    purpose: icarEnums.icarStatisticsPurposeType = Field(
        json_schema_extra={"description": "Defines the purpose for these statistics."},
    )
    dateFrom: icarTypes.icarDateType = Field(
        json_schema_extra={
            "description": "The start of the period for which statistics are calculated."
        },
    )
    dateTo: icarTypes.icarDateType = Field(
        json_schema_extra={
            "description": "The end of the period for which statistics are calculated."
        },
    )
    group: list[icarTypes.icarStatisticsGroupType] = Field(
        json_schema_extra={
            "description": "An array of groups for which statistics are calculated, each of which has statistics for that group."
        },
    )


class icarEventCoreResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarEventCoreResource.__name__)
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique identifier in the source system for this event."
        },
    )
    eventDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date and time (see https://ijmacd.github.io/rfc3339-iso8601/)."
        },
    )
    traitLabel: Optional[icarTypes.icarTraitLabelIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "If the event represents a formal trait, identifies the recording system and trait."
        },
    )
    responsible: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Use if an observation is manually recorded, or an event is carried out or authorised by a person. SHOULD be a person object."
        },
    )
    contemporaryGroup: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "For manually recorded events, record any contemporary group code that would affect statistical analysis."
        },
    )
    remark: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A comment or remark field for additional user-specified information about the event."
        },
    )


class icarAnimalEventCoreResource(icarEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarAnimalEventCoreResource.__name__
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )


class icarAnimalCoreResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarAnimalCoreResource.__name__)
    identifier: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    alternativeIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Alternative identifiers for the animal. Here, also temporary identifiers, e.g. transponders or animal numbers, can be listed."
        },
    )
    specie: icarEnums.icarAnimalSpecieType = Field(
        json_schema_extra={"description": "Species of the animal."},
    )
    gender: icarEnums.icarAnimalGenderType = Field(
        json_schema_extra={"description": "Gender of the animal."},
    )
    birthDate: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time of birth (see https://ijmacd.github.io/rfc3339-iso8601/ for how to use)."
        },
    )
    primaryBreed: Optional[icarTypes.icarBreedIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "ICAR Breed code for the animal."},
    )
    breedFractions: Optional[icarTypes.icarBreedFractionsType] = Field(
        default=None,
        json_schema_extra={"description": "Breed fractions for the animal."},
    )
    coatColor: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Colour of the animal's coat, using the conventions for that breed."
        },
    )
    coatColorIdentifier: Optional[icarTypes.icarCoatColorIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Colour of the animal's coat using a national or breed-defined scheme and identifier combination."
        },
    )
    managementTag: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The identifier used by the farmer in day to day operations. In many cases this could be the animal number."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Name given by the farmer for this animal."},
    )
    officialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name."},
    )
    productionPurpose: Optional[icarEnums.icarProductionPurposeType] = Field(
        default=None,
        json_schema_extra={
            "description": "Primary production purpose for which animals are bred."
        },
    )
    status: Optional[icarEnums.icarAnimalStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "On-farm status of the animal (such as alive, dead, off-farm)."
        },
    )
    reproductionStatus: Optional[icarEnums.icarAnimalReproductionStatusType] = Field(
        default=None,
        json_schema_extra={"description": "Reproduction status of the animal."},
    )
    lactationStatus: Optional[icarEnums.icarAnimalLactationStatusType] = Field(
        default=None,
        json_schema_extra={"description": "Lactation status of the animal."},
    )
    parentage: Optional[list[icarTypes.icarParentageType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Parents of the animal.  The array can handle multiple generations by specifying the parent of a parent."
        },
    )
    healthStatus: Optional[icarEnums.icarAnimalHealthStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "Health status of the animal (such as Healthy, Suspicious, Ill, InTreatment, ToBeCulled)."
        },
    )


class icarMovementBirthEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMovementBirthEventResource.__name__
    )
    registrationReason: Optional[icarEnums.icarRegistrationReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies whether this is a birth or a registration event"
        },
    )
    animalDetail: Optional[icarAnimalCoreResource] = Field(
        default=None,
        json_schema_extra={
            "description": "Core animal details.  Can be used if the animal has not already been defined on the holding."
        },
    )


class icarGestationResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarGestationResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this computed resource."
        },
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    sireIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique scheme/identifier combinations for the sire, including official ID and Herdbook."
        },
    )
    expectedCalvingDate: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "The RFC3339 UTC date the calving is expected to happen (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )


class icarDailyMilkingAveragesResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarDailyMilkingAveragesResource.__name__
    )
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique identifier in the source system for this event."
        },
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    averageDate: icarTypes.icarDateType = Field(
        json_schema_extra={
            "description": "The date on which the average has been calculated."
        },
    )
    milkYieldAvg24h: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The average-amount of milk produced within 24h."
        },
    )
    milkYieldAvg7days: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The average-amount of milk produced within 7 days."
        },
    )


class icarTreatmentEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarTreatmentEventResource.__name__
    )
    medicine: Optional[icarTypes.icarMedicineReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "A reference to the medicine used (where applicable)."
        },
    )
    procedure: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Medicine application method or a non-medicine procedure."
        },
    )
    batches: Optional[list[icarTypes.icarMedicineBatchType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Batches and expiry details for the medicine administered."
        },
    )
    withdrawals: Optional[list[icarTypes.icarMedicineWithdrawalType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Withholding details for the treatment administered."
        },
    )
    dose: Optional[icarTypes.icarMedicineDoseType] = Field(
        default=None,
        json_schema_extra={"description": "Details of medicine dose administered"},
    )
    site: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Body site where the treatment was administered."
        },
    )
    positions: Optional[list[icarTypes.icarPositionType]] = Field(
        default=None,
        json_schema_extra={"description": "The positions to be treated"},
    )
    comment: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A comment recorded about the treatment or its outcome."
        },
    )


class icarTreatmentProgramEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarTreatmentProgramEventResource.__name__
    )
    diagnoses: Optional[list[icarTypes.icarDiagnosisType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Decribes the diagnosis of one or more conditions"
        },
    )
    courses: Optional[list[icarTypes.icarMedicineCourseSummaryType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Details the course of treatments at a summary (start and end date) level. The array allows for different medicines/procedures."
        },
    )
    treatments: Optional[list[icarTreatmentEventResource]] = Field(
        default=None,
        json_schema_extra={
            "description": "The list of the treatments (medicines or procedures) applied."
        },
    )


class icarReproMatingRecommendationResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproMatingRecommendationResource.__name__
    )
    sireRecommendations: Optional[list[icarTypes.icarSireRecommendationType]] = Field(
        default=None,
    )


class exampleErrorResource(FTModel):
    resourceType: str = Field(default_factory=lambda: exampleErrorResource.__name__)
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A unique identifier for this particular occurrence of the problem"
        },
    )
    status: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The HTTP status code applicable to this problem, expressed as a string value"
        },
    )
    code: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "An application-specific error code, expressed as a string value."
        },
    )
    title: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A short, human-readable summary of the problem that SHOULD NOT change from occurrence to occurrence of the problem, except for purposes of localization."
        },
    )
    detail: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A human-readable explanation specific to this occurrence of the problem. Like title, this field’s value can be localized."
        },
    )
    meta: Optional[None] = Field(
        default=None,
    )


class icarResourceCollectionReference(FTModel):
    resourceType: str = Field(
        default_factory=lambda: icarResourceCollectionReference.__name__
    )
    id: str = Field(
        json_schema_extra={
            "description": "Uniform resource idendentifier (URI) of the collection."
        },
    )
    type: str = Field(
        json_schema_extra={
            "description": "Specifies whether this is a single resource Link or a Collection."
        },
    )
    context: str = Field(
        json_schema_extra={
            "description": "Tells us the type of the referenced resource object (eg. icarAnimalCoreCollection)."
        },
    )
    totalItems: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Provides the number of items in the collection, if known."
        },
    )
    pageSize: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "If non-zero, specifies the default number of items returned per page."
        },
    )
    totalPages: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Provides the number of pages in the collection, if known."
        },
    )
    operations: Optional[list[(None, None)]] = Field(
        default=None,
        json_schema_extra={
            "description": "Defines the operations that may be carried out on the collection (POST) or its members (PUT/PATCH/DELETE)."
        },
    )


class icarFeedIntakeEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarFeedIntakeEventResource.__name__
    )
    feedingStartingDateTime: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "The RFC3339 UTC moment the feeding started (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    feedVisitDuration: icarTypes.icarFeedDurationType = Field()
    consumedFeed: Optional[list[icarTypes.icarConsumedFeedType]] = Field(
        default=None,
    )
    consumedRation: Optional[icarTypes.icarConsumedRationType] = Field(
        default=None,
        json_schema_extra={"description": "The eventual ration that has been consumed"},
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for the feeding."
        },
    )


class icarLocationResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarLocationResource.__name__)
    identifier: icarTypes.icarLocationIdentifierType = Field(
        json_schema_extra={
            "description": "Unique location scheme and identifier combination."
        },
    )
    alternativeIdentifiers: Optional[list[icarTypes.icarLocationIdentifierType]] = (
        Field(
            default=None,
            json_schema_extra={
                "description": "Alternative identifiers for the location. Must be a 1:1 mapping, meaning that when querying resources with an alternative identifier (instead of the 'main' identifier), the response may not be different."
            },
        )
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The human readable name of the location."},
    )
    timeZoneId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The time zone ID of the location according to the IANA time zone database (https://www.iana.org/time-zones), e.g. Europe/Paris. Can be used to convert UTC times in events, resources etc. back to the locations time zone while also taking daylight saving times into account."
        },
    )


class icarMedicineTransactionResource(icarTypes.icarInventoryTransactionType):
    resourceType: str = Field(
        default_factory=lambda: icarMedicineTransactionResource.__name__
    )
    product: icarTypes.icarMedicineReferenceType = Field(
        json_schema_extra={"description": "The medicine product in this transaction."},
    )


class icarTestDayResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarTestDayResource.__name__)
    id: str = Field(
        json_schema_extra={"description": "Unique identifier for this test day."},
    )
    beginDate: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "The RFC3339 UTC datetime of the beginning of the milk sampling (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    endDate: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "The RFC3339 UTC datetime of the end of the milk sampling (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )


class icarMovementDepartureEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMovementDepartureEventResource.__name__
    )
    departureKind: Optional[icarEnums.icarDepartureKindType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the kind of departure of the animal from the holding."
        },
    )
    departureReason: Optional[icarEnums.icarDepartureReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the reason for the departure of the animal from the holding."
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the animal from the holding."
        },
    )
    extendedReasons: Optional[list[icarTypes.icarReasonIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Extended reason codes why this animal has departed."
        },
    )


class icarCarcassResource(icarResource, icarTypes.icarCarcassType):
    resourceType: str = Field(default_factory=lambda: icarCarcassResource.__name__)


class icarAnimalSetResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarAnimalSetResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this animal set."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Human readable name of the set."},
    )
    reference: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "This property can be used by parties for any other reference information used to synchronise systems or display to the user."
        },
    )
    purpose: Optional[icarEnums.icarSetPurposeType] = Field(
        default=None,
        json_schema_extra={"description": "Purpose of the animal set."},
    )
    member: list[icarTypes.icarAnimalIdentifierType] = Field(
        json_schema_extra={
            "description": "As per JSON-LD Hydra syntax, member provides the array of objects, in this case animals assigned to the set."
        },
    )


class icarGroupEventCoreResource(icarEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupEventCoreResource.__name__
    )
    groupMethod: icarEnums.icarGroupEventMethodType = Field(
        json_schema_extra={
            "description": "Indicates whether the event references an existing animal set, has an embedded animal set, or an inventory classification."
        },
    )
    countObserved: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Summarises the number of animals observed in the event. Generally the number of animals in the group, but sometimes a sample."
        },
    )
    inventoryClassification: Optional[icarTypes.icarInventoryClassificationType] = (
        Field(
            default=None,
            json_schema_extra={
                "description": "Describe the group of animals by their characteristics rather than animal identifiers."
            },
        )
    )
    embeddedAnimalSet: Optional[icarAnimalSetResource] = Field(
        default=None,
        json_schema_extra={
            "description": "Specifies the set of animals as a list of member animal identifiers."
        },
    )
    animalSetReference: Optional[icarTypes.icarAnimalSetReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Reference an existing animal set by ID and optionally URI"
        },
    )


class icarGroupMovementArrivalEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupMovementArrivalEventResource.__name__
    )
    arrivalReason: icarEnums.icarArrivalReasonType = Field(
        json_schema_extra={
            "description": "Reason the group of animals arrived on the holding."
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the group of animals to the holding."
        },
    )


class icarReproPregnancyCheckEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproPregnancyCheckEventResource.__name__
    )
    method: Optional[icarEnums.icarReproPregnancyMethodType] = Field(
        default=None,
        json_schema_extra={"description": "Method by which diagnosis was carried out."},
    )
    result: Optional[icarEnums.icarReproPregnancyResultType] = Field(
        default=None,
        json_schema_extra={"description": "Result - unknown, empty, pregnant."},
    )
    foetalAge: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Assessed age of the foetus or length of the pregnancy (in days)."
        },
    )
    foetusCount: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "If specified, contains the number of foetuses observed."
        },
    )
    foetusCountMale: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "If specified, contains number of foetuses observed as male."
        },
    )
    foetusCountFemale: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "If specified, contains number of foetuses observed as female."
        },
    )
    exceptions: Optional[list[str]] = Field(
        default=None,
        json_schema_extra={
            "description": "Additional local observations - such as ABNORMAL CALF"
        },
    )


class icarFeedReportResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarFeedReportResource.__name__)
    animals: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "As per JSON-LD Hydra syntax, animals provides the array of animals part of the feeding report. This could also be a report for one animal."
        },
    )
    reportStartDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC moment the period of the reporting started (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    reportEndDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC moment the period of the reporting ended (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    feedVisitDuration: Optional[icarTypes.icarFeedDurationType] = Field(
        default=None,
    )
    consumedFeed: Optional[list[icarTypes.icarConsumedFeedType]] = Field(
        default=None,
    )
    consumedRation: Optional[list[icarTypes.icarConsumedRationType]] = Field(
        default=None,
    )


class icarBreedingValueResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarBreedingValueResource.__name__
    )
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this event."
        },
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    base: Optional[icarTypes.icarBVBaseIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The scheme and the id of the base of the breeding value."
        },
    )
    version: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": " string which sets the version for the breeding value estimation - this can be a date, or a version name, or something the calculation center is using to identify their seperate runs."
        },
    )
    breedingValues: Optional[list[icarTypes.icarBreedingValueType]] = Field(
        default=None,
    )


class icarAnimalSetLeaveEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarAnimalSetLeaveEventResource.__name__
    )
    animalSetId: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for the animal set to be left."
        },
    )


class icarPositionObservationEventResource(
    icarAnimalEventCoreResource, icarTypes.icarPositionObservationType
):
    resourceType: str = Field(
        default_factory=lambda: icarPositionObservationEventResource.__name__
    )


class icarSchemeValueResource(FTModel):
    resourceType: str = Field(default_factory=lambda: icarSchemeValueResource.__name__)
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Id/identifier for scheme value."},
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Friendly name for scheme value."},
    )


class icarDeviceResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarDeviceResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier on location level in the source system for this device."
        },
    )
    serial: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Optionally, the serial number of the device."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Name given to the device by the farmer."},
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Description of the device by the farmer."},
    )
    softwareVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Version of the software installed on the device."
        },
    )
    hardwareVersion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Version of the hardware installed in the device."
        },
    )
    isActive: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicates whether the device is active at this moment."
        },
    )
    supportedMessages: Optional[list[(None, None)]] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies message types supported for the device"
        },
    )
    manufacturer: Optional[icarTypes.icarDeviceManufacturerType] = Field(
        default=None,
        json_schema_extra={
            "description": "The device data as defined by the manufacturer."
        },
    )
    registration: Optional[icarTypes.icarDeviceRegistrationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "A registration identifier for the device (most devices should eventually have a registration issued by `org.icar` or other entity)."
        },
    )


class icarResponseMessageResource(FTModel):
    resourceType: str = Field(
        default_factory=lambda: icarResponseMessageResource.__name__
    )
    type: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Machine readable URI or code that defines the type of error or warning."
        },
    )
    severity: Optional[icarEnums.icarBatchResultSeverityType] = Field(
        default=None,
        json_schema_extra={
            "description": "Distinguish errors, warnings, and informational messages."
        },
    )
    status: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The HTTP status code applicable to this problem."
        },
    )
    title: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A short, human-readable summary of the problem that SHOULD NOT change from occurrence to occurrence of the problem, except for purposes of localization."
        },
    )
    detail: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A human-readable explanation specific to this occurrence of the problem. Like title, this field’s value can be localized."
        },
    )
    instance: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A URI reference or internal JSON document reference to the specific data item that caused the problem."
        },
    )


class icarWithdrawalEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarWithdrawalEventResource.__name__
    )
    endDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date and time (see https://ijmacd.github.io/rfc3339-iso8601/)."
        },
    )
    productType: icarEnums.icarWithdrawalProductType = Field(
        json_schema_extra={
            "description": "Product or food item affected by this withdrawal."
        },
    )


class icarBatchResult(FTModel):
    resourceType: str = Field(default_factory=lambda: icarBatchResult.__name__)
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique identifier created in the system for this event. SHOULD be a UUID."
        },
    )
    meta: Optional[icarTypes.icarMetaDataType] = Field(
        default=None,
        json_schema_extra={
            "description": "Metadata for the posted resource. Allows specification of the source, source Id to synchronise data."
        },
    )
    messages: Optional[list[None]] = Field(
        default=None,
        json_schema_extra={
            "description": "An array of errors for this resource. The messages array may be unspecified OR null."
        },
    )


class icarGroupFeedingEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupFeedingEventResource.__name__
    )
    feedingEndDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC moment from which animals could no longer consume the feed (eventDateTime represents the start of feed availability)."
        },
    )
    feedPerAnimal: Optional[list[icarTypes.icarConsumedFeedType]] = Field(
        default=None,
    )
    feedTotal: Optional[list[icarTypes.icarConsumedFeedType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Gives the feed offered to and consumed (total for all animals)."
        },
    )
    rationPerAnimal: Optional[list[icarTypes.icarConsumedRationType]] = Field(
        default=None,
    )
    rationTotal: Optional[list[icarTypes.icarConsumedRationType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Gives the feed offered to and consumed (total for all animals)."
        },
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about a device used for the feeding, if relevant."
        },
    )


class icarFeedRecommendationResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarFeedRecommendationResource.__name__
    )
    id: icarTypes.icarFeedRecommendationIdType = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this recommendation."
        },
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    recommendationDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC timestamp of the recommendation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    startDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC date of the beginning of the recommendation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    endDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC end date of the recommendation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    recommendedFeed: Optional[list[icarTypes.icarRecommendedFeedType]] = Field(
        default=None,
    )
    recommendedRation: Optional[list[icarTypes.icarRecommendedRationType]] = Field(
        default=None,
    )


class icarReproHeatEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproHeatEventResource.__name__
    )
    heatDetectionMethod: Optional[icarEnums.icarReproHeatDetectionMethodType] = Field(
        default=None,
    )
    certainty: Optional[icarEnums.icarReproHeatCertaintyType] = Field(
        default=None,
    )
    commencementDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time when the heat will start (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    expirationDateTime: Optional[FutureDatetime] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time when the heat will end (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    visualDetection: Optional[None] = Field(
        default=None,
        json_schema_extra={
            "description": "Specific info when the heat was visually detected."
        },
    )
    optimumInseminationWindow: Optional[list[icarTypes.icarReproHeatWindowType]] = (
        Field(
            default=None,
            json_schema_extra={
                "description": "Details of the optimum breeding windows"
            },
        )
    )
    deviceHeatProbability: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The manufacturer specific indication for the certainty of the heat"
        },
    )
    heatReportScrSenseTime: Optional[None] = Field(
        default=None,
        json_schema_extra={
            "description": "Specific info when the heat was detected by SenseTime from SCR"
        },
    )
    heatReportNedapCowControl: Optional[None] = Field(
        default=None,
        json_schema_extra={
            "description": "Specific info when the heat was detected by CowControl from NEDAP"
        },
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for the measurement."
        },
    )


class icarReproSemenStrawResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproSemenStrawResource.__name__
    )
    id: Optional[icarTypes.icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Official identifier for the straw (if any)."
        },
    )
    batch: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Identification of the batch of semen."},
    )
    collectionCentre: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Identifies the collection centre."},
    )
    dateCollected: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time of collection (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    sireIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "One or more unique scheme/identifier combinations for the sire."
        },
    )
    sireOfficialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name of the sire."},
    )
    sireURI: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "URI to an AnimalCoreResource for the sire."},
    )
    preservationType: Optional[icarEnums.icarReproSemenPreservationType] = Field(
        default=None,
        json_schema_extra={
            "description": "The method of preservation of the semen (liquid, frozen)."
        },
    )
    isSexedSemen: Optional[bool] = Field(
        default=None,
        json_schema_extra={"description": "True if this is sexed semen."},
    )
    sexedGender: Optional[icarEnums.icarAnimalGenderType] = Field(
        default=None,
        json_schema_extra={
            "description": "Specify Male or Female for sexed semen only."
        },
    )
    sexedPercentage: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Percentage of semen that are expected to be of the chosen sex (e.g. 75, 90, 95)."
        },
    )


class icarFeedTransactionResource(icarTypes.icarInventoryTransactionType):
    resourceType: str = Field(
        default_factory=lambda: icarFeedTransactionResource.__name__
    )
    product: icarTypes.icarFeedReferenceType = Field(
        json_schema_extra={"description": "The feed product in this transaction."},
    )


class icarGroupWeightEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupWeightEventResource.__name__
    )
    units: Optional[icarEnums.uncefactMassUnitsType] = Field(
        default=None,
        json_schema_extra={
            "description": "Units specified in UN/CEFACT 3-letter form. Default if not specified is KGM."
        },
    )
    method: Optional[icarEnums.icarWeightMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "The method of observation. Loadcell is the default if not specified."
        },
    )
    resolution: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The smallest measurement difference that can be discriminated given the current device settings. Specified in Units, for instance 0.5 (kilograms)."
        },
    )
    animalWeights: Optional[list[icarTypes.icarIndividualWeightType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Array of animal id and weight pairs for animals in the event."
        },
    )
    statistics: Optional[list[icarTypes.icarStatisticsType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Array of weight statistics, namely average, sum, min, max, count, stdev"
        },
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for the measurement."
        },
    )
    timeOffFeed: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Hours of curfew or withholding feed prior to weighing to standardise gut fill."
        },
    )


class icarWeightEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(default_factory=lambda: icarWeightEventResource.__name__)
    weight: Optional[icarTypes.icarMassMeasureType] = Field(
        default=None,
        json_schema_extra={
            "description": "The weight measurement, including units and resolution."
        },
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for the measurement."
        },
    )
    timeOffFeed: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Hours of curfew or withholding feed prior to weighing to standardise gut fill."
        },
    )


class icarDiagnosisEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarDiagnosisEventResource.__name__
    )
    diagnoses: Optional[list[icarTypes.icarDiagnosisType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Diagnosis of the animal health condition. An array allows for several conditions to be recorded at once."
        },
    )


class icarInventoryTransactionResource(icarTypes.icarInventoryTransactionType):
    resourceType: str = Field(
        default_factory=lambda: icarInventoryTransactionResource.__name__
    )
    product: icarTypes.icarProductReferenceType = Field(
        json_schema_extra={"description": "The product in this inventory transaction."},
    )


class icarLactationStatusObservedEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarLactationStatusObservedEventResource.__name__
    )
    observedStatus: Optional[icarEnums.icarAnimalLactationStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "The lactation status at the time of observation."
        },
    )


class icarMovementDeathEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMovementDeathEventResource.__name__
    )
    deathReason: Optional[icarEnums.icarDeathReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Coded reasons for death including disease, parturition complications, consumption by humans or animals."
        },
    )
    explanation: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Free text explanation of the reason for death."
        },
    )
    disposalMethod: Optional[icarEnums.icarDeathDisposalMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "Coded disposal methods including approved service, consumption by humans or animals, etc."
        },
    )
    disposalOperator: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Disposal operator official name (should really be schema.org/organization)."
        },
    )
    disposalReference: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Reference (receipt, docket, or ID) for disposal."
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the animal from the holding."
        },
    )
    deathMethod: Optional[icarEnums.icarDeathMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "Defines the method of death, including an accident, natural causes, or euthanised."
        },
    )
    extendedReasons: Optional[list[icarTypes.icarReasonIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Extended reason codes why this animal has died."
        },
    )


class icarReproParturitionEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproParturitionEventResource.__name__
    )
    isEmbryoImplant: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "True if the progeny is the result of an embryo implant."
        },
    )
    damParity: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The calving, litter, or other parturition number for the dam"
        },
    )
    liveProgeny: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of live offspring from the parturition. Important if progeny are not identified."
        },
    )
    totalProgeny: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The total number of offspring from the parturition, including those born dead."
        },
    )
    calvingEase: Optional[icarEnums.icarReproCalvingEaseType] = Field(
        default=None,
        json_schema_extra={
            "description": "Calving ease (enum corresponds to traditional 1-5 values)."
        },
    )
    progenyDetails: Optional[list[None]] = Field(
        default=None,
        json_schema_extra={
            "description": "List of progeny details. May not be fully identified, but recommend that gender and status are supplied at least."
        },
    )
    progeny: Optional[list[None]] = Field(
        default=None,
        json_schema_extra={
            "description": "List of progeny. May not be fully identified, but recommend that gender and status are supplied at least."
        },
    )


class icarGroupTreatmentEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupTreatmentEventResource.__name__
    )
    medicine: Optional[icarTypes.icarMedicineReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "A reference to the medicine used (where applicable)."
        },
    )
    procedure: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Medicine application method or a non-medicine procedure."
        },
    )
    batches: Optional[list[icarTypes.icarMedicineBatchType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Batches and expiry details for the medicine administered."
        },
    )
    withdrawals: Optional[list[icarTypes.icarMedicineWithdrawalType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Withholding details for the treatment administered."
        },
    )
    dosePerAnimal: Optional[icarTypes.icarMedicineDoseType] = Field(
        default=None,
        json_schema_extra={
            "description": "The actual or average medicine dose administered per animal."
        },
    )
    totalMedicineUsed: Optional[icarTypes.icarMedicineDoseType] = Field(
        default=None,
        json_schema_extra={"description": "The total amount of medicine used."},
    )
    site: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Body site where the treatment was administered."
        },
    )
    positions: Optional[list[icarTypes.icarPositionType]] = Field(
        default=None,
        json_schema_extra={"description": "The positions to be treated"},
    )


class icarConformationScoreEventResource(
    icarAnimalEventCoreResource, icarTypes.icarConformationScoreType
):
    resourceType: str = Field(
        default_factory=lambda: icarConformationScoreEventResource.__name__
    )


class icarRationResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarRationResource.__name__)
    id: icarTypes.icarRationIdType = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this resource."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name of the feed as it is known on the location."
        },
    )
    feeds: Optional[list[icarTypes.icarFeedsInRationType]] = Field(
        default=None,
    )
    active: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "indicates whether the ration is or was available on the location."
        },
    )


class icarAttentionEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarAttentionEventResource.__name__
    )
    alertEndDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 date time that represents the end time of an alert (start time is the eventDateTime) if it has ended."
        },
    )
    category: icarEnums.icarAttentionCategoryType = Field(
        json_schema_extra={
            "description": "A category that allows filtering of alerts by subject."
        },
    )
    causes: list[icarEnums.icarAttentionCauseType] = Field(
        json_schema_extra={
            "description": "The specific causes of the alert. This is an array and at least one cause must be specified."
        },
    )
    priority: Optional[icarEnums.icarAttentionPriorityType] = Field(
        default=None,
        json_schema_extra={"description": "The relative priority of the alert."},
    )
    severity: Optional[icarEnums.icarDiagnosisSeverityType] = Field(
        default=None,
        json_schema_extra={
            "description": "A structured set of severity values that align with those used in disease diagnosis."
        },
    )
    deviceAttentionScore: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Provides a manufacturer- and device-specific score related to the alert."
        },
    )
    device: Optional[icarTypes.icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the device that is raising the alert."
        },
    )


class icarLactationResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarLactationResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this event."
        },
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    beginDate: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC date of the beginning of the lactation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    endDate: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC end date of the the lactation. This occurs when the animal is dried off, dies or calves again."
        },
    )
    parity: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The parity of the animal during this lactation."
        },
    )
    lactationLength: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The length of the lactation until this moment."
        },
    )
    milkAmount: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of milk produced in this lactation."
        },
    )
    fatAmount: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of fat produced in this lactation."
        },
    )
    proteinAmount: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of protein produced in this lactation."
        },
    )
    lactosisAmount: Optional[icarTypes.icarTraitAmountType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of lactosis produced in this lactation."
        },
    )
    lastTestDay: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RCF3339 UTC date of the last test day in the lactation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    lactationType: Optional[icarEnums.icarLactationType] = Field(
        default=None,
        json_schema_extra={
            "description": "This type of lactation based on lactation length that is delivered."
        },
    )
    milkRecordingMethod: Optional[icarTypes.icarMilkRecordingMethodType] = Field(
        default=None,
    )


class icarReproInseminationEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproInseminationEventResource.__name__
    )
    rank: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The rank of intervention of each AI carried out within the same reproductive cycle."
        },
    )
    inseminationType: icarEnums.icarReproInseminationType = Field()
    sireIdentifiers: Optional[list[icarTypes.icarAnimalIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique scheme/identifier combinations for the sire, including official ID and Herdbook."
        },
    )
    sireOfficialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name of the sire."},
    )
    sireURI: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "URI to an AnimalCoreResource for the sire."},
    )
    straw: Optional[icarReproSemenStrawResource] = Field(
        default=None,
        json_schema_extra={
            "description": "Details of the straw, which may also include sire details."
        },
    )
    eventEndDateTime: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "To be used in case of running with a bull to end the period. RFC3339 UTC format (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    semenFromFarmStocks: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "True if the semen is from the farmer's own stocks (false if supplied by technician)."
        },
    )
    farmContainer: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Number or ID of the container from which the dose was taken."
        },
    )
    embryo: Optional[icarReproEmbryoResource] = Field(
        default=None,
        json_schema_extra={"description": "Details of the embryo."},
    )


class icarSortingSiteResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarSortingSiteResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the system for this site."
        },
    )
    name: str = Field(
        json_schema_extra={
            "description": "Name of the site as it is known on the location."
        },
    )
    capacity: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The maximum capacity of this site."},
    )


class icarMedicineResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarMedicineResource.__name__)
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name of the medicine or remedy given for this treatment"
        },
    )
    approved: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "An indicator whether the medicine or remedy is an approved medicine"
        },
    )
    registeredID: Optional[icarTypes.icarMedicineIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "Registered ID in the scheme and ID format."},
    )


class icarMovementArrivalEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMovementArrivalEventResource.__name__
    )
    arrivalReason: Optional[icarEnums.icarArrivalReasonType] = Field(
        default=None,
        json_schema_extra={"description": "Reason the animal arrived on the holding."},
    )
    animalDetail: Optional[icarAnimalCoreResource] = Field(
        default=None,
        json_schema_extra={
            "description": "Core animal details. Can be used if the animal has not already been defined on the holding."
        },
    )
    animalState: Optional[icarTypes.icarAnimalStateType] = Field(
        default=None,
        json_schema_extra={"description": "State information about an animal."},
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the consignment of the animal to the holding."
        },
    )


class icarAnimalSortingCommandResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarAnimalSortingCommandResource.__name__
    )
    animal: icarTypes.icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    sites: list[str] = Field(
        json_schema_extra={
            "description": "Array with unique site identifiers where this animal can be sorted to."
        },
    )
    validFrom: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "Specifies from when the sort command should be active. RFC3339 UTC date time (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    validTo: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "Specifies until when the sort command should be active. Could be left empty, when the sorting should be ongoing (until replaced). RFC3339 UTC date time (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )


class icarMilkingVisitEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMilkingVisitEventResource.__name__
    )
    milkingStartingDateTime: icarTypes.icarDateTimeType = Field(
        json_schema_extra={
            "description": "The RFC3339 UTC date time of the start of milking (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    milkingDuration: Optional[icarTypes.icarMilkDurationType] = Field(
        default=None,
    )
    milkingVisitDuration: Optional[icarTypes.icarMilkDurationType] = Field(
        default=None,
    )
    milkingType: Optional[icarEnums.icarMilkingTypeCode] = Field(
        default=None,
        json_schema_extra={
            "description": "This code allows organisations to distinguish between manual and automated milking."
        },
    )
    milkingMilkWeight: icarTypes.icarMilkingMilkWeightType = Field(
        json_schema_extra={
            "description": "A certified milking weight that complies with the ICAR guidelines."
        },
    )
    milkingComplete: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "indication whether this milking was completed normally."
        },
    )
    milkingParlourUnit: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The milking parlour unit where the milking took place."
        },
    )
    milkingBoxNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The milking box number where the milking took place."
        },
    )
    milkingDeviceId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The ID of the device where the milking took place."
        },
    )
    measureDeviceId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The ID of the device where the measurement of the milking took place"
        },
    )
    milkingShiftLocalStartDate: Optional[icarTypes.icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The ISO8601 date in local time zone to which this milking shift belongs. A time component is not expected or required."
        },
    )
    milkingShiftNumber: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "For milkings supervised by humans, this number represents the shift within a local date in which this milking visit occurred."
        },
    )
    quarterMilkings: Optional[list[icarTypes.icarQuarterMilkingType]] = Field(
        default=None,
        json_schema_extra={
            "description": "A set of milking results for up to four quarters in dairy cows, or two teats for sheep or goats."
        },
    )
    animalMilkingSample: Optional[list[icarTypes.icarAnimalMilkingSampleType]] = Field(
        default=None,
        json_schema_extra={
            "description": "An array of zero or more sample/bottle details if the animal is milk tested at this milking."
        },
    )
    milkCharacteristics: Optional[list[icarTypes.icarMilkCharacteristicsType]] = Field(
        default=None,
        json_schema_extra={
            "description": "An array of milk characteristics other than certified milk weight. See icarMilkCharacteristicsType for documentation."
        },
    )
    milkingRemarks: Optional[list[icarEnums.icarMilkingRemarksType]] = Field(
        default=None,
    )


class icarFeedStorageResource(icarDeviceResource):
    resourceType: str = Field(default_factory=lambda: icarFeedStorageResource.__name__)
    feedId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique identifier of the feed that is stored in this device."
        },
    )
    capacity: Optional[icarTypes.icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed that can be stored in this device."
        },
    )
    quantityAvailable: Optional[icarTypes.icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed that is currently stored in this device and is available for feeding."
        },
    )


class icarAnimalSetJoinEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarAnimalSetJoinEventResource.__name__
    )
    animalSetId: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for the animal set to be joined."
        },
    )


class icarHealthStatusObservedEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarHealthStatusObservedEventResource.__name__
    )
    observedStatus: Optional[icarEnums.icarAnimalHealthStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "Health status of the animal (such as Healthy, Suspicious, Ill, InTreatment, ToBeCulled). A null value is not supported."
        },
    )


class icarGroupPositionObservationEventResource(
    icarGroupEventCoreResource, icarTypes.icarPositionObservationType
):
    resourceType: str = Field(
        default_factory=lambda: icarGroupPositionObservationEventResource.__name__
    )


class icarProgenyDetailsResource(icarResource):
    resourceType: str = Field(
        default_factory=lambda: icarProgenyDetailsResource.__name__
    )
    identifier: Optional[None] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    alternativeIdentifiers: Optional[list[None]] = Field(
        default=None,
        json_schema_extra={
            "description": "Alternative identifiers for the animal. Here, also temporary identifiers, e.g. transponders or animal numbers, can be listed."
        },
    )
    specie: icarEnums.icarAnimalSpecieType = Field(
        json_schema_extra={"description": "Species of the animal."},
    )
    gender: icarEnums.icarAnimalGenderType = Field(
        json_schema_extra={"description": "Gender of the animal."},
    )
    managementTag: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The identifier used by the farmer in day to day operations. In many cases this could be the animal number."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Name given by the farmer for this animal."},
    )
    officialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name."},
    )
    taggingDate: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Progeny tagging date in RFC3339 UTC (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    birthStatus: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Birth status of the progeny."},
    )
    birthSize: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Size of the progeny."},
    )
    birthWeight: Optional[None] = Field(
        default=None,
        json_schema_extra={"description": "Weight of the progeny."},
    )


class icarCarcassObservationsEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarCarcassObservationsEventResource.__name__
    )
    carcass: Optional[icarTypes.icarCarcassType] = Field(
        default=None,
        json_schema_extra={"description": "The carcass being observed."},
    )
    observations: Optional[list[icarTypes.icarCarcassObservationType]] = Field(
        default=None,
        json_schema_extra={
            "description": "The array of observations performed in this event"
        },
    )
    side: Optional[icarEnums.icarCarcassSideType] = Field(
        default=None,
        json_schema_extra={
            "description": "The side of the carcass observed in this event (use Both if not split)."
        },
    )
    primal: Optional[icarEnums.icarCarcassPrimalType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the primal being observed (`Total` if not split)."
        },
    )
    carcassState: Optional[icarEnums.icarCarcassStateType] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicates whether the observation event is on the hot or cold (chilled) carcass."
        },
    )
    device: Optional[icarDeviceResource] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the device used for performing the observations in this event."
        },
    )


class icarMilkPredictionResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMilkPredictionResource.__name__
    )
    averagePredictedProduction: Optional[icarTypes.icarMilkingPredictionType] = Field(
        default=None,
    )
    daysInMilkAtLactationPeak: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The days in milk in a lactation when the peak production is expected to occur."
        },
    )
    lactationPeakProduction: Optional[icarTypes.icarMilkingPredictionType] = Field(
        default=None,
    )
    predictedProductionNextMR: Optional[icarTypes.icarMilkingPredictionType] = Field(
        default=None,
    )


class icarReproDoNotBreedEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproDoNotBreedEventResource.__name__
    )
    doNotBreed: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "Set this attribute to true if the animal should not be bred, false if it may now be bred."
        },
    )
    extendedReasons: Optional[list[icarTypes.icarReasonIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Extended reason codes why this animal should not be bred."
        },
    )


class icarTestDayResultEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarTestDayResultEventResource.__name__
    )
    milkWeight24Hours: Optional[icarTypes.icarMilkingMilkWeightType] = Field(
        default=None,
    )
    testDayCode: Optional[icarEnums.icarTestDayCodeType] = Field(
        default=None,
    )
    milkCharacteristics: Optional[list[icarTypes.icarMilkCharacteristicsType]] = Field(
        default=None,
    )
    predictedProductionOnTestDay: Optional[icarTypes.icarMilkingPredictionType] = Field(
        default=None,
    )


class icarReproEmbryoFlushingEventResource(icarEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproEmbryoFlushingEventResource.__name__
    )
    flushingMethod: icarEnums.icarReproEmbryoFlushingMethodType = Field()
    embryoCount: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of embryos extracted in the flushing."
        },
    )
    collectionCentre: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The location where the embryo was flushed."},
    )


class icarGroupMovementBirthEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupMovementBirthEventResource.__name__
    )
    registrationReason: icarEnums.icarRegistrationReasonType = Field(
        json_schema_extra={
            "description": "Identifies whether this is a birth or registration event"
        },
    )


class icarMilkingDryOffEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarMilkingDryOffEventResource.__name__
    )


class icarReproStatusObservedEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproStatusObservedEventResource.__name__
    )
    observedStatus: Optional[icarEnums.icarAnimalReproductionStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "The reproductive status at the time of observation."
        },
    )


class icarFeedResource(icarResource):
    resourceType: str = Field(default_factory=lambda: icarFeedResource.__name__)
    id: str = Field(
        json_schema_extra={
            "description": "Unique identifier in the source system for this resource."
        },
    )
    category: Optional[icarEnums.icarFeedCategoryType] = Field(
        default=None,
        json_schema_extra={
            "description": "The scheme and the id of the category of the feed."
        },
    )
    type: Optional[icarTypes.icarFeedIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The scheme and the id of the type of the feed. ICAR recommends the use of the list of the scheme org.fao"
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name of the feed as it is known on the location."
        },
    )
    properties: Optional[list[icarTypes.icarFeedPropertyType]] = Field(
        default=None,
    )
    active: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "indicates whether the feed is or was available on the location."
        },
    )


class icarProcessingLotResource(icarResource, icarTypes.icarProcessingLotType):
    resourceType: str = Field(
        default_factory=lambda: icarProcessingLotResource.__name__
    )


class icarGroupMovementDeathEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupMovementDeathEventResource.__name__
    )
    deathreason: Optional[icarEnums.icarDeathReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Coded reason for death - this is the CAUSE, compared to the MEANS."
        },
    )
    explanation: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Free text explanation of the reason for death."
        },
    )
    disposalMethod: Optional[icarEnums.icarDeathDisposalMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "Coded disposal methods including approved service, consumption by humans or animals, etc."
        },
    )
    disposalOperator: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Disposal operator official name (should really be schema.org/organization)."
        },
    )
    disposalReference: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Reference (receipt, docket, or ID) for disposal."
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Where disposal is by transport, a consignment record may be required."
        },
    )
    deathMethod: icarEnums.icarDeathMethodType = Field(
        json_schema_extra={
            "description": "Defines the MEANS of death, including an accident, natural causes, or euthanised."
        },
    )


class icarGroupMovementDepartureEventResource(icarGroupEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarGroupMovementDepartureEventResource.__name__
    )
    departureKind: icarEnums.icarDepartureKindType = Field(
        json_schema_extra={
            "description": "Coded description of the type of departure (e.g. sale, agistment, other)."
        },
    )
    departureReason: Optional[icarEnums.icarDepartureReasonType] = Field(
        default=None,
        json_schema_extra={
            "description": "Coded description of the reason why the animals are departing."
        },
    )
    consignment: Optional[icarTypes.icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Consignment information about origin, destination, and transport."
        },
    )


class icarReproAbortionEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarReproAbortionEventResource.__name__
    )


class icarTypeClassificationEventResource(icarAnimalEventCoreResource):
    resourceType: str = Field(
        default_factory=lambda: icarTypeClassificationEventResource.__name__
    )
    conformationScores: Optional[list[icarTypes.icarConformationScoreType]] = Field(
        default=None,
    )
