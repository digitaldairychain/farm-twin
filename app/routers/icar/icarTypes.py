"""
Collection of types used in ICAR data standards.
See here for more details: https://github.com/adewg/ICAR/blob/v1.4.1/enums
"""

from typing import Optional

from geojson_pydantic import GeometryCollection
from pydantic import BaseModel, Field, PastDatetime

from . import icarEnums


class icarFeedDurationType(BaseModel):
    unitCode: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "UN/CEFACT Common Code for Units of Measurement."
        },
    )
    value: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The duration of the feeding in the units specified."
        },
    )


class icarIdentifierType(BaseModel):
    id: str = Field(
        json_schema_extra={
            "description": "A unique identification for the resource issued under the auspices of the scheme."
        },
    )
    scheme: str = Field(
        json_schema_extra={
            "description": "The identifier (in reverse domain format) of an official scheme that manages unique identifiers."
        },
    )


class icarCarcassMetricIdentifierType(icarIdentifierType):
    pass


class icarCarcassMetricType(BaseModel):
    id: Optional[icarCarcassMetricIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The id of the metric expressed as a scheme and id."
        },
    )
    method: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The standard method used to determine the value of the metric."
        },
    )
    qualifier: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Qualifier applied to further describe the metric (if any)."
        },
    )


class icarTraitLabelIdentifierType(icarIdentifierType):
    pass


class icarBreedingValueType(BaseModel):
    traitLabel: Optional[icarTraitLabelIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The scheme and id of the trait for which a breeding value is calculated"
        },
    )
    calculationType: Optional[icarEnums.icarBreedingValueCalculationType] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicates the calculation method/type for the breeding value."
        },
    )
    value: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The breeding value."},
    )
    reliability: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The reliability of the breeding value"},
    )
    resolution: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The smallest difference that is relevant for this breeding value (to guide display). To assist in the interpretation of floating point values."
        },
    )


class icarFeedQuantityType(BaseModel):
    unitCode: icarEnums.uncefactMassUnitsType = Field(
        json_schema_extra={
            "description": "Units specified in UN/CEFACT 3-letter form. Default if not specified is KGM."
        },
    )
    value: float = Field(
        json_schema_extra={"description": "The feed quantity in the units specified."},
    )


class icarDiagnosisIdentifierType(icarIdentifierType):
    pass


class icarMilkDurationType(BaseModel):
    unitCode: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "UN/CEFACT Common Code for Units of Measurement."
        },
    )
    value: Optional[float] = Field(
        default=None,
    )


class icarMilkingMilkWeightType(BaseModel):
    unitCode: str = Field(
        json_schema_extra={
            "description": "UN/CEFACT Common Code for Units of Measurement."
        },
    )
    value: float = Field()


class icarMilkCharacteristicsType(BaseModel):
    characteristic: str = Field(
        json_schema_extra={
            "description": "Treat this field as an enum, with the list and units in https://github.com/adewg/ICAR/blob/v1.4.1/enums/icarMilkCharacteristicCodeType.json."
        },
    )
    value: str = Field(
        json_schema_extra={"description": "the value of the characteristic measured"},
    )
    unit: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Use the units for characteristics in https://github.com/adewg/ICAR/blob/v1.4.1/enums/icarMilkCharacteristicCodeType.json. Only override when your units for a characteristic are different. Use UN/CEFACT codes."
        },
    )
    measuringDevice: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "a more readable device class ID that contains manufacturer, device, hardware and software versions in a way that is similar to the USB specification. This will need more investigation."
        },
    )


class icarQuarterMilkingSampleType(BaseModel):
    bottleIdentifierType: Optional[icarEnums.icarBottleIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The type of bottle identifiertype according to ICAR_BottleIdentifierCode"
        },
    )
    rackNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Number of the sample rack"},
    )
    bottlePosition: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Position of the bottle in the sample rack"},
    )
    bottleIdentifier: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Bottle identifier read from barcode or RFID"
        },
    )
    validSampleFillingIndicator: Optional[
        icarEnums.icarValidSampleFillingIndicatorType
    ] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicator of valid sample filling according to ICAR_ValidSampleFillingIndicatorCode list"
        },
    )
    operator: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The operator that took the sample"},
    )


class icarQuarterMilkingType(BaseModel):
    icarQuarterId: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "the unique id of the quarter milking"},
    )
    xposition: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional milking robot X position. Vendors may choose not to provide this."
        },
    )
    yposition: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional milking robot Y position. Vendors may choose not to provide this."
        },
    )
    zposition: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional milking robot Z position. Vendors may choose not to provide this."
        },
    )
    quarterMilkingDuration: Optional[icarMilkDurationType] = Field(
        default=None,
    )
    quarterMilkingWeight: Optional[icarMilkingMilkWeightType] = Field(
        default=None,
    )
    icarQuarterMilkingSample: Optional[list[icarQuarterMilkingSampleType]] = Field(
        default=None,
    )
    icarQuarterCharacteristics: Optional[list[icarMilkCharacteristicsType]] = Field(
        default=None,
    )


class icarFeedRecommendationIdType(BaseModel):
    pass


class icarOrganizationIdentityType(BaseModel):
    name: str = Field(
        json_schema_extra={"description": "Name of the organisation"},
    )
    leiCode: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "An organization identifier that uniquely identifies a legal entity as defined in ISO 17442."
        },
    )
    globalLocationNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The Global Location Number (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations."
        },
    )
    uri: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A uniform resource identifier that is the unique reference or for this organisation, such as its web site."
        },
    )


class icarOrganizationIdentifierType(icarIdentifierType):
    pass


class PostalAddress(BaseModel):
    addressCountry: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code."
        },
    )
    addressLocality: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The locality in which the street address is, and which is in the region. For example, Mountain View."
        },
    )
    addressRegion: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The region in which the locality is, and which is in the country. For example, California or another appropriate first-level Administrative division"
        },
    )
    postOfficeBoxNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The post office box number for PO box addresses."
        },
    )
    postalCode: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The postal code. For example, 94043."},
    )
    streetAddress: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The street address. For example, 1600 Amphitheatre Pkwy."
        },
    )


class icarOrganizationType(icarOrganizationIdentityType):
    establishmentIdentifiers: Optional[list[icarOrganizationIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Scheme and identifier combinations that provide official registrations for a business or establishment"
        },
    )
    address: Optional[PostalAddress] = Field(
        default=None,
        json_schema_extra={
            "description": "Postal address or physical address in postal format, including country. Optional as this may already be specified in a consignment."
        },
    )
    parentOrganization: Optional[icarOrganizationIdentityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The larger organization that this organization is a sub-organization of, if any."
        },
    )
    membershipIdentifiers: Optional[list[icarOrganizationIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Scheme and identifier combinations that identity membership in programmes"
        },
    )


class icarDateTimeType(PastDatetime):
    pass


class icarInterestedPartyType(icarOrganizationType):
    pass


class icarLocationIdentifierType(icarIdentifierType):
    pass


class icarDeclarationIdentifierType(icarIdentifierType):
    pass


class icarConsignmentDeclarationType(BaseModel):
    declarationId: Optional[icarDeclarationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the specific declaration being made using a scheme and an id."
        },
    )
    declaredValue: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The value of the declaration."},
    )


class icarConsignmentType(BaseModel):
    id: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "Official identifier for the movement."},
    )
    originLocation: Optional[icarLocationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The location of the origin of the consignment expressed as a scheme and id."
        },
    )
    originAddress: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Origin address for movement."},
    )
    originPostalAddress: Optional[PostalAddress] = Field(
        default=None,
        json_schema_extra={
            "description": "A structured, schema.org-style address for the origin location."
        },
    )
    originOrganization: Optional[icarOrganizationType] = Field(
        default=None,
        json_schema_extra={
            "description": "The organisational details of the origin, including any necessary identifiers."
        },
    )
    destinationLocation: Optional[icarLocationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The location of the destination of the consignment expressed as a scheme and id."
        },
    )
    destinationAddress: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Destination address for movement."},
    )
    destinationPostalAddress: Optional[PostalAddress] = Field(
        default=None,
        json_schema_extra={
            "description": "A structured, schema.org-style address for the destination location."
        },
    )
    destinationOrganization: Optional[icarOrganizationType] = Field(
        default=None,
        json_schema_extra={
            "description": "The organisational details of the destination, including any necessary identifiers."
        },
    )
    loadingDateTime: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date and time animals were loaded for transport (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    unloadingDateTime: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date and time animals were unloaded after transport (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    expectedDuration: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Expected duration of transportation in hours."
        },
    )
    transportOperator: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Transport operator official name (should really be schema.org/organization)."
        },
    )
    vehicle: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Identification of the vehicle (for example, licence plate)."
        },
    )
    transportReference: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Shipping or transporter reference."},
    )
    isolationFacilityUsed: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "True if an isolation facility was used for the movement."
        },
    )
    farmAssuranceReference: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identification reference of a farm assurance operation."
        },
    )
    countConsigned: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of animals despatched or consigned from the origin."
        },
    )
    countReceived: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of animals received at the destination."
        },
    )
    hoursOffFeed: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of hours since animals in the consignment had access to feed."
        },
    )
    hoursOffWater: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of hours since animals in the consignment had access to water."
        },
    )
    references: Optional[list[icarIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "References associated with the consignment. These may be additional to the single transport reference (for instance, to support multi-mode transport)."
        },
    )
    interestedParties: Optional[list[icarInterestedPartyType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the parties and their interests in the consignment."
        },
    )
    declarations: Optional[list[icarConsignmentDeclarationType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Country, species or scheme -specific declarations for the consignment."
        },
    )


class icarPlantChainType(BaseModel):
    plant: icarOrganizationType = Field(
        json_schema_extra={
            "description": "Identifies the plant using an Organization object."
        },
    )
    chainId: str = Field(
        json_schema_extra={
            "description": "A within-plant identifier for the processing chain. This might be a name or numeric code."
        },
    )
    chainProcess: Optional[icarEnums.icarChainProcessType] = Field(
        default=None,
        json_schema_extra={
            "description": "Whether the part of the processing chain involved is before (Ante) or after (Post) mortem."
        },
    )


class icarProcessingLotType(BaseModel):
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A plant internal identifier to uniquely identify the processing lot. This should be a UUID or otherwise unique."
        },
    )
    name: str = Field(
        json_schema_extra={
            "description": "A name or visual identifier allocated by the plant to the lot."
        },
    )
    chain: icarPlantChainType = Field(
        json_schema_extra={
            "description": "The processing plant and chain for this lot."
        },
    )
    killDateTime: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The date and time at which killing on the lot started"
        },
    )
    startBodyNumber: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Ordinal of the first body or carcass in lot counting across same plant, chain and kill date"
        },
    )
    endBodyNumber: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Ordinal of the last body or carcass in lot counting across same plant, chain and kill date"
        },
    )
    lotCount: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of animals (bodies for a processor) processed in this lot."
        },
    )
    targetMarket: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Represents the intended market for the stock.  It is defined by the processor and may be mapped to industry grids or schedules."
        },
    )
    killType: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The processor's internal classification code"
        },
    )
    species: icarEnums.icarAnimalSpecieType = Field(
        json_schema_extra={
            "description": "The animal species being processed in the lot"
        },
    )
    consignment: Optional[icarConsignmentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Details of the inbound consignment from which animals in this lot are drawn."
        },
    )
    interestedParties: Optional[list[icarInterestedPartyType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the parties and their interests in the processing lot."
        },
    )


class icarBreedIdentifierType(icarIdentifierType):
    pass


class icarAnimalIdentifierType(icarIdentifierType):
    pass


class icarCarcassType(BaseModel):
    processingLot: icarProcessingLotType = Field(
        json_schema_extra={
            "description": "The lot in which the carcass was processed. "
        },
    )
    killDateTime: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "Date/time the animal was killed. Ideally this should be a precise date and time. However, older systems may only be able to supply the date."
        },
    )
    bodyNo: int = Field(
        json_schema_extra={
            "description": "A unique identifier on the chain and kill date  assigned to the carcass by the processor."
        },
    )
    identifiers: list[icarAnimalIdentifierType] = Field(
        json_schema_extra={
            "description": "Identifiers for the carcass including the animal's id"
        },
    )
    sex: Optional[icarEnums.icarAnimalGenderType] = Field(
        default=None,
        json_schema_extra={
            "description": "The sex of the animal as assessed at the processing plant."
        },
    )
    birthDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "Assessed date of birth of the animal represented using RFC3339 (UTC)."
        },
    )
    birthDateConfidence: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A 3-character string representing Year, Month, and Day (YMD). Each character can have the value A (actual), E (estimate), U (unknown). e.g. AEU."
        },
    )
    primaryBreed: Optional[icarBreedIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Primary breed of the animal as visually categorised by the plant, represented using ICAR breed codes."
        },
    )
    plantBoningRun: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "Allocation of the carcass to a plant boning run (if any)."
        },
    )
    plantBoningRunTemplate: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Where a Boning Run Template is allocated by the plant, the name or ID of the template."
        },
    )
    destinationCode: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Plant-specific destination codes that are used for company requirements and to link to boning run processing."
        },
    )
    processorGrid: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Reference to a processor-specific grid used to calculate the price paid to the producer"
        },
    )


class icarResourceReferenceType(BaseModel):
    context: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Deprecated. Tells us the type of the referenced resource object (eg. icarAnimalCore)."
        },
    )
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Deprecated - use href and identifier. Uniform resource idendentifier (URI) of the referenced resource."
        },
    )
    type: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Deprecated - use reltype. Specifies whether this is a single resource Link or a Collection."
        },
    )
    identifier: Optional[icarIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Provides the identifier of the referenced resource."
        },
    )
    reltype: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Defines the relationship between the current resource and the referenced resource. Defined in well-known/relationshipCatalog.md"
        },
    )
    href: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Where provided, this is the URI to the referenced resource."
        },
    )


class icarAnimalSetReferenceType(icarResourceReferenceType):
    pass


class icarMetaDataType(BaseModel):
    source: str = Field(
        json_schema_extra={
            "description": "Source where data is retrieved from. URI  or reverse DNS that identifies the source system."
        },
    )
    sourceId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique Id within Source (e.g. UUID, IRI, URI, or composite ID if needed) for the resource in the original source system.  Systems should generate (if needed), store, and return sourceId if at all possible.ICAR ADE working group intend to make use of metadata, source and sourceId mandatory in the next major release (2.0)."
        },
    )
    isDeleted: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "Boolean value indicating if this resource has been deleted in the source system."
        },
    )
    modified: PastDatetime = Field(
        json_schema_extra={
            "description": "RFC3339 UTC date/time of last modification (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    created: Optional[PastDatetime] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time of creation (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    creator: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Person or organisation who created the object"
        },
    )
    validFrom: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC start of period when the resource is valid (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    validTo: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC end of the period when the resoure is valid (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )


class icarBVBaseIdentifierType(icarIdentifierType):
    pass


class icarCoatColorIdentifierType(icarIdentifierType):
    pass


class icarMedicineWithdrawalType(BaseModel):
    productType: Optional[icarEnums.icarWithdrawalProductType] = Field(
        default=None,
        json_schema_extra={
            "description": "Product or food item affected by this withdrawal."
        },
    )
    endDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC end date of withdrawal calculated based on treatment date and medicine rules (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    market: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The market to which the withdrawal applies, using a scheme such as au.gov.apvma.esi or au.gov.apvma.whp"
        },
    )


class icarPositionType(BaseModel):
    position: Optional[icarEnums.icarPositionOnAnimalType] = Field(
        default=None,
        json_schema_extra={
            "description": "Position on the animal where the diagnosis or treatment occurred."
        },
    )


class icarDeviceRegistrationIdentifierType(icarIdentifierType):
    pass


class icarDeviceReferenceType(icarResourceReferenceType):
    model: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "ICAR registered device model, which represents manufacturer, model, hardware and software versions."
        },
    )
    serial: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Optionally, the serial number of the device."
        },
    )
    manufacturerName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The manufacturer of the device. This is called `manufacturerName` to distinguish it from the manufacturer-specific parameters in icarDevice."
        },
    )
    registration: Optional[icarDeviceRegistrationIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "A registration identifier for the device (most devices should eventually have a registration issued by `org.icar` or other entity)."
        },
    )


class icarConformationScoreType(BaseModel):
    traitGroup: Optional[icarEnums.icarConformationTraitGroupType] = Field(
        default=None,
        json_schema_extra={
            "description": "Defines whether the trait is a composite trait or a linear trait."
        },
    )
    score: float = Field(
        json_schema_extra={
            "description": "Conformation score with values of 1 to 9 numeric in case of linear traits and for composites in most cases between 50 and 99"
        },
    )
    traitScored: icarEnums.icarConformationTraitType = Field(
        json_schema_extra={
            "description": "Scored conformation trait type according ICAR guidelines. See https://www.icar.org/Guidelines/05-Conformation-Recording.pdf"
        },
    )
    method: Optional[icarEnums.icarConformationScoringMethodType] = Field(
        default=None,
        json_schema_extra={"description": "Method of conformation scoring"},
    )
    device: Optional[icarDeviceReferenceType] = Field(
        default=None,
        json_schema_extra={
            "description": "Optional information about the device used for the automated scoring."
        },
    )


class icarFeedIdentifierType(icarIdentifierType):
    pass


class icarFeedsInRationType(BaseModel):
    feedId: Optional[icarFeedIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "identifies the feed"},
    )
    percentage: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "the percentage of the feed in the ration."},
    )


class icarCarcassObservationType(BaseModel):
    metric: icarCarcassMetricType = Field(
        json_schema_extra={"description": "The metric observed."},
    )
    value: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The observed value of the metric if it is numeric."
        },
    )
    units: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The units in which the value is measured. UN/CEFACT units SHOULD be used for metrics where these are applicable."
        },
    )
    resolution: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The smallest measurement difference that can be discriminated. Specified in the units, for instance 0.5 (kilograms)."
        },
    )
    qualitativeValue: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The observed value of the metric if it is a grade or other string."
        },
    )
    observationStatus: Optional[icarEnums.icarObservationStatusType] = Field(
        default=None,
        json_schema_extra={"description": "The status of the observation."},
    )
    remark: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The reason if there is an issue with the observation"
        },
    )


class icarMassMeasureType(BaseModel):
    measurement: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The weight observation, in the units specified (usually kilograms)."
        },
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


class icarRationIdType(icarIdentifierType):
    pass


class icarCostType(BaseModel):
    currency: str = Field(
        json_schema_extra={
            "description": "The currency of the cost expressed using the ISO 4217 3-character code (such as AUD, GBP, USD, EUR)."
        },
    )
    value: float = Field(
        json_schema_extra={"description": "The costs in the units specified."},
    )


class icarConsumedRationType(BaseModel):
    rationId: icarRationIdType = Field(
        json_schema_extra={"description": "The identifier for the ration consumed"},
    )
    entitlement: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group was entitled to receive"
        },
    )
    delivered: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group received. If not present, it can be assumed that the delivered will be equal to entitlement"
        },
    )
    feedConsumption: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group has consumed"
        },
    )
    dryMatterPercentage: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The dry matter content of the ration provided or consumed, expressed as a percentage."
        },
    )
    totalCost: Optional[icarCostType] = Field(
        default=None,
        json_schema_extra={
            "description": "Total cost applied to this feeding. Based on the delivered or entitled amount"
        },
    )


class icarIndividualWeightType(BaseModel):
    animal: Optional[icarAnimalIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    weight: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The weight measurement"},
    )


class icarReasonIdentifierType(icarIdentifierType):
    pass


class icarMedicineBatchType(BaseModel):
    identifier: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The ID, batch or lot number."},
    )
    expiryDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The RFC3339 UTC expiry date of the batch (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )


class icarRecommendedFeedType(BaseModel):
    feedId: Optional[icarFeedIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "The identifier for the feed recommended"},
    )
    entitlement: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal is recommended to reveive"
        },
    )


class icarMetricType(icarIdentifierType):
    pass


class icarStatisticsType(BaseModel):
    metric: Optional[icarMetricType] = Field(
        default=None,
        json_schema_extra={
            "description": "The metric code for a specific statistics. See https://github.com/adewg/ICAR/wiki/Schemes for more info"
        },
    )
    unit: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The unit of the metric. This must be appropriate to the metric and UN-CEFACT unit codes should be used where possible."
        },
    )
    aggregation: Optional[icarEnums.icarAggregationType] = Field(
        default=None,
        json_schema_extra={"description": "The aggregation applied to the metric."},
    )
    value: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The value of the metric."},
    )


class icarGroupSpecifierType(BaseModel):
    lactationNumberRangeMin: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "minimum number of lactations for the animals in the group."
        },
    )
    lactationNumberRangeMax: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "maximum number of lactations for the animals in the group."
        },
    )
    daysInMilkRangeMin: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "minimum number of days in milk for the animals in the group."
        },
    )
    daysInMilkRangeMax: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "maximum number of days in milk for the animals in the group."
        },
    )
    animalSetId: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique identifier in the source system for this animal set."
        },
    )


class icarStatisticsGroupType(BaseModel):
    icarGroupType: Optional[icarEnums.icarGroupType] = Field(
        default=None,
    )
    denominator: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "Number of animals in the group."},
    )
    icarGroupSpecifier: Optional[list[icarGroupSpecifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "A set of group specifiers that in combination define the animals in the group."
        },
    )
    statistics: Optional[list[icarStatisticsType]] = Field(
        default=None,
        json_schema_extra={"description": "An array of statistics for this group."},
    )


class icarProductIdentifierType(icarIdentifierType):
    pass


class icarDateType(PastDatetime):
    pass


class icarProductReferenceType(icarResourceReferenceType):
    identifiers: Optional[list[icarProductIdentifierType]] = Field(
        default=None,
        json_schema_extra={
            "description": "An array of product identifiers. This allows a product to have multiple identifiers for manufacturers, distributors, official registrations, etc."
        },
    )
    family: icarEnums.icarProductFamilyType = Field(
        json_schema_extra={
            "description": "The product family to which this product belongs."
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The name of the product."},
    )
    gtin: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "GS1 global trade item number."},
    )
    unspc: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "UN service and product code (the code, not the accompanying description)."
        },
    )


class icarFeedReferenceType(icarProductReferenceType):
    category: Optional[icarEnums.icarFeedCategoryType] = Field(
        default=None,
        json_schema_extra={"description": "Defines the category of the feed product."},
    )
    type: Optional[icarFeedIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The scheme + id identifying the type of feed."
        },
    )


class icarMilkRecordingMethodType(BaseModel):
    milkRecordingProtocol: Optional[icarEnums.icarMilkRecordingProtocolType] = Field(
        default=None,
        json_schema_extra={
            "description": "Protocol A: Official MRO representative, Protocol B: Herd owner or its nominee, Protocol C: Official MRO representative or herd owner or its nominee."
        },
    )
    milkRecordingScheme: Optional[icarEnums.icarMilkRecordingSchemeType] = Field(
        default=None,
        json_schema_extra={
            "description": "all milkings at testday, all milkings in period, one milking at testday."
        },
    )
    milkingsPerDay: Optional[icarEnums.icarMilkingsPerDayType] = Field(
        default=None,
        json_schema_extra={
            "description": "1 per day, 2, 3, 4, Continuous Milkings (e.g. robotic milking)."
        },
    )
    milkSamplingScheme: Optional[icarEnums.icarMilkSamplingSchemeType] = Field(
        default=None,
        json_schema_extra={
            "description": "proportional size sampling of all milkings, constant size sampling of all milkings, sampling of one milking at alternating moments (Alternative Sampling), sampling of one milking at the same moments (Corrected Sampling), sampling of one milking at changing moments (AMS), sampling of multiple milkings at changing moments (AMS)."
        },
    )
    recordingInterval: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "A number in days of the interval between milk recordings. In case of e.g.4 weeks, use 30."
        },
    )
    milkSamplingMoment: Optional[icarEnums.icarMilkSamplingMomentType] = Field(
        default=None,
        json_schema_extra={
            "description": "Composite = composite sample from morning and evening, Morning, Evening."
        },
    )
    icarCertified: Optional[bool] = Field(
        default=None,
        json_schema_extra={
            "description": "indicates whether this information is certified by ICAR"
        },
    )
    milkingType: Optional[icarEnums.icarMilkingType] = Field(
        default=None,
        json_schema_extra={
            "description": "Official milk result supplied by milk recording organisation, Measure by ICAR approved equipment, Measure by not approved equipment"
        },
    )


class icarSireRecommendationType(BaseModel):
    recommendationType: Optional[icarEnums.icarRecommendationType] = Field(
        default=None,
    )
    sireIdentifiers: Optional[list[icarAnimalIdentifierType]] = Field(
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
    parity: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The parity of the cow for which the recommendation is valid."
        },
    )
    sireRank: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The rank of the sire in the recommendation, 1 = first choice, 2 = second, ...."
        },
    )


class icarInventoryTransactionType(BaseModel):
    transactionKind: icarEnums.icarInventoryTransactionKindType = Field(
        json_schema_extra={"description": "Identifies the transaction kind."},
    )
    quantity: float = Field(
        json_schema_extra={
            "description": "The overall volume, weight or count of the product in the transaction in the units defined."
        },
    )
    units: str = Field(
        json_schema_extra={
            "description": "The units of the quantity specified.  Where applicable it is recommended that uncefact mass and volume units are used."
        },
    )
    supplierName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The supplier of the product in this transaction.  This is particularly relevant if the transaction is a receipt."
        },
    )
    expiryDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "The expiry date of the product supplied in the transaction."
        },
    )
    totalCost: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "Total cost applied to this transaction"},
    )
    currency: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The currency of the cost expressed using the ISO 4217 3-character code (such as AUD, GBP, USD, EUR)."
        },
    )
    packSize: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The volume or weight of the product in a pack in the units defined. Especially relevant for Vet Medicines."
        },
    )
    numberOfPacks: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of packs of the product in the transaction. Especially relevant for Vet Medicines. Could be a decimal number for a part-pack."
        },
    )


class icarMedicineIdentifierType(icarIdentifierType):
    pass


class icarMedicineDoseType(BaseModel):
    doseQuantity: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Quantity of medicine or product administered."
        },
    )
    doseUnits: Optional[icarEnums.uncefactDoseUnitsType] = Field(
        default=None,
        json_schema_extra={
            "description": "Units of measurement in UN/CEFACT 3-letter form"
        },
    )


class icarMedicineReferenceType(icarProductReferenceType):
    approved: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "An indicator whether the medicine or remedy is an approved medicine"
        },
    )
    registeredIdentifier: Optional[icarMedicineIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The registered identifier of the medicine expressed as a scheme and id."
        },
    )


class icarMedicineCourseSummaryType(BaseModel):
    startDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC start date of the treatment course (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)"
        },
    )
    endDate: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC End date of the treatment course (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)"
        },
    )
    medicine: Optional[icarMedicineReferenceType] = Field(
        default=None,
        json_schema_extra={"description": "Medicine details used in the course."},
    )
    procedure: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Medicine application method or non-medicine procedure."
        },
    )
    site: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Body site where the treatment or procedure was administered."
        },
    )
    reasonForAdministration: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "This attribute can be used when medicine has been administered without a diagnosis"
        },
    )
    totalDose: Optional[icarMedicineDoseType] = Field(
        default=None,
        json_schema_extra={"description": "Total dose proposed or administered."},
    )
    numberOfTreatments: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of treatments included in the course."
        },
    )
    treatmentInterval: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "The interval between treatments specified in HOURS."
        },
    )
    batches: Optional[list[icarMedicineBatchType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Batches and expiry details of the medicine (there may be several)."
        },
    )
    planOrActual: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicator showing if the attributes in the course Summary are actual information for the treatments or the plan"
        },
    )
    withdrawals: Optional[list[icarMedicineWithdrawalType]] = Field(
        default=None,
        json_schema_extra={
            "description": "Provides withholding details for the treatment administered"
        },
    )


class icarInventoryClassificationType(BaseModel):
    name: str = Field(
        json_schema_extra={
            "description": "Human-readable name for this inventory grouping."
        },
    )
    count: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The count or number of animals in this inventory classification."
        },
    )
    species: icarEnums.icarAnimalSpecieType = Field(
        json_schema_extra={"description": "The species of animals."},
    )
    sex: Optional[icarEnums.icarAnimalGenderType] = Field(
        default=None,
        json_schema_extra={"description": "The sex of animals."},
    )
    primaryBreed: Optional[icarBreedIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Primary breed defined using an identifier and scheme."
        },
    )
    birthPeriod: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The range of birth dates. Use YYYY (all one year), YYYY-MM (one month), or two RFC3339 date-times separated by / to represent a range."
        },
    )
    reproductiveStatus: Optional[icarEnums.icarAnimalReproductionStatusType] = Field(
        default=None,
        json_schema_extra={
            "description": "The reproductive/pregnancy status of animals."
        },
    )
    lactationStatus: Optional[icarEnums.icarAnimalLactationStatusType] = Field(
        default=None,
        json_schema_extra={"description": "The lactation status of animals."},
    )
    productionPurposes: Optional[list[icarEnums.icarProductionPurposeType]] = Field(
        default=None,
        json_schema_extra={"description": "Array of production purposes."},
    )
    reference: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "An external reference (identifier or name) to further identify the group of animals."
        },
    )


class icarAnimalStateType(BaseModel):
    currentLactationParity: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "The current parity of the animal."},
    )
    lastCalvingDate: Optional[icarDateType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date (see https://ijmacd.github.io/rfc3339-iso8601/)."
        },
    )
    lastInseminationDate: Optional[icarDateType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date (see https://ijmacd.github.io/rfc3339-iso8601/)."
        },
    )
    lastDryingOffDate: Optional[icarDateType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date (see https://ijmacd.github.io/rfc3339-iso8601/)."
        },
    )


class icarAnimalIdType(BaseModel):
    pass


class icarConsumedFeedType(BaseModel):
    feedId: icarFeedIdentifierType = Field(
        json_schema_extra={"description": "The identifier for the feed consumed"},
    )
    entitlement: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group was entitled to receive"
        },
    )
    delivered: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group received. If not present, it can be assumed that the delivered will be equal to entitlement"
        },
    )
    feedConsumption: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of feed the animal/group has consumed"
        },
    )
    dryMatterPercentage: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The dry matter content of the feed provided or consumed, expressed as a percentage."
        },
    )
    totalCost: Optional[icarCostType] = Field(
        default=None,
        json_schema_extra={
            "description": "Total cost applied to this feeding. Based on the delivered or entitled amount"
        },
    )


class icarTraitAmountType(BaseModel):
    unitCode: str = Field(
        json_schema_extra={
            "description": "UN/CEFACT Common Code for Units of Measurement."
        },
    )
    value: float = Field()


class icarBreedFractionsType(BaseModel):
    denominator: int = Field(
        json_schema_extra={
            "description": "The denominator of breed fractions - for instance 16, 64, or 100."
        },
    )
    fractions: Optional[list[(None, None)]] = Field(
        default=None,
        json_schema_extra={
            "description": "The numerators of breed fractions for each breed proportion."
        },
    )


class icarDeviceManufacturerType(BaseModel):
    id: str = Field(
        json_schema_extra={
            "description": "Unique id of the manufacturer. Domain name/url --> lely.com, …"
        },
    )
    deviceType: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "A device type registered within the database proposed by the Sensor Working Group. This could be a UUID but we prefer a meaningful string."
        },
    )
    deviceName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name given to the device by the manufacturer."
        },
    )
    deviceDescription: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Description of the device by the manufacturer."
        },
    )
    deviceConfiguration: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Configuration of the device."},
    )


class icarMilkingPredictionType(BaseModel):
    milkWeight: icarMilkingMilkWeightType = Field()
    fatWeight: Optional[icarMilkingMilkWeightType] = Field(
        default=None,
    )
    proteinWeight: Optional[icarMilkingMilkWeightType] = Field(
        default=None,
    )
    hours: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "The number of hours in which the mentioned milk, fat and protein were produced. Most commonly used is a 24 hours production."
        },
    )


class icarPropertyIdentifierType(icarIdentifierType):
    pass


class icarFeedPropertyType(BaseModel):
    propertyIdentifier: Optional[icarPropertyIdentifierType] = Field(
        default=None,
        json_schema_extra={"description": "identifies the property of the feed"},
    )
    value: Optional[float] = Field(
        default=None,
        json_schema_extra={"description": "the value of the property."},
    )
    units: Optional[icarEnums.uncefactMassUnitsType] = Field(
        default=None,
        json_schema_extra={
            "description": "Units specified in UN/CEFACT 3-letter form. Default if not specified is KGM."
        },
    )
    method: Optional[icarEnums.icarMethodType] = Field(
        default=None,
        json_schema_extra={
            "description": "The method to come to the value of the property"
        },
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "name of the property (used on the location)."
        },
    )


class icarAnimalMilkingSampleType(BaseModel):
    bottleIdentifierType: Optional[icarEnums.icarBottleIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "The type of bottle identifiertype according to ICAR_BottleIdentifierCode"
        },
    )
    rackNumber: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Number of the sample rack"},
    )
    bottlePosition: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Position of the bottle in the sample rack"},
    )
    bottleIdentifier: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Bottle identifier read from barcode or RFID"
        },
    )
    validSampleFillingIndicator: Optional[
        icarEnums.icarValidSampleFillingIndicatorType
    ] = Field(
        default=None,
        json_schema_extra={
            "description": "Indicator of valid sample filling according to ICAR_ValidSampleFillingIndicatorCode list"
        },
    )
    operator: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "The operator that took the sample"},
    )


class icarDiagnosisType(BaseModel):
    id: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Unique identifier for this diagnosis."},
    )
    name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Name indicating the health condition diagnosed."
        },
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Description of the diagnosis or problem."},
    )
    diagnosisCode: Optional[icarDiagnosisIdentifierType] = Field(
        default=None,
        json_schema_extra={
            "description": "Descibes the scheme (eg venom or ICAR) and the code (ID) within that scheme."
        },
    )
    site: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Site on the animal involved in the diagnosis or disease."
        },
    )
    stage: Optional[icarEnums.icarDiagnosisStageType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the clinical stage of disease progression."
        },
    )
    severity: Optional[icarEnums.icarDiagnosisSeverityType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies the clinical severity of the problem."
        },
    )
    severityScore: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "description": "Clinical severity expressed as a numeric score for systems that record this."
        },
    )
    positions: Optional[list[icarPositionType]] = Field(
        default=None,
        json_schema_extra={"description": "The positions to be treated"},
    )


class icarReproHeatWindowType(BaseModel):
    startDateTime: icarDateTimeType = Field(
        json_schema_extra={
            "description": "RFC3339 UTC date/time when the optimum insemination window starts (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    endDateTime: Optional[icarDateTimeType] = Field(
        default=None,
        json_schema_extra={
            "description": "RFC3339 UTC date/time when the optimum insemination window ends (see https://ijmacd.github.io/rfc3339-iso8601/ for format guidance)."
        },
    )
    windowName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The name of the optimum insemination breeding window."
        },
    )


class icarParentageType(BaseModel):
    parentOf: icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "References the child of this parent (allowing you to build multi-generation pedigrees)."
        },
    )
    gender: icarEnums.icarAnimalGenderType = Field(
        json_schema_extra={
            "description": "Specifies Male or Female gender so you can recognise Sire or Dam."
        },
    )
    relation: Optional[icarEnums.icarAnimalRelationType] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifies type of parent: Genetic (default), Recipient, Adoptive (Foster/Rearing)."
        },
    )
    identifier: icarAnimalIdentifierType = Field(
        json_schema_extra={
            "description": "Unique animal scheme and identifier combination."
        },
    )
    officialName: Optional[str] = Field(
        default=None,
        json_schema_extra={"description": "Official herdbook name."},
    )


class icarPositionObservationType(BaseModel):
    positionName: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "The name of a location, such as a barn, pen, building, or field."
        },
    )
    site: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Identifier for a sorting site (icarSortingSiteResource) for this position."
        },
    )
    geometry: Optional[GeometryCollection] = Field(
        default=None,
        json_schema_extra={
            "description": "A GeoJSON geometry (such as a latitude/longitude point) that specifies the position."
        },
    )


class icarRecommendedRationType(BaseModel):
    rationId: Optional[icarRationIdType] = Field(
        default=None,
        json_schema_extra={"description": "The identifier for the ration recommended"},
    )
    entitlement: Optional[icarFeedQuantityType] = Field(
        default=None,
        json_schema_extra={
            "description": "The amount of this ration the animal is recommended to receive"
        },
    )
