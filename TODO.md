# { farm-twin } TODO #

Add experiment endpoint as a collection of things and attachments
Add a documentation endpoint for adding context to data - markdown?
Interface for managing data - related object discovery?
Ensure UTC conformance for times
source field: tell me where the data came from

Is a timestamp missing from conformation?
Stop modified and created values being passed
Stop ft being changed in updates (need to check)

Compliance with ICAR: https://github.com/adewg/ICAR/wiki/Resource-entities
    - animal set/collections?
    - medicine
    - ration
    - embryo
    - sementstraw

ICAR not implemented: 
set join
set leave
groupevent(s)


Python datetime -> ICAR Datetime format/type
align ft device/machine? -> https://github.com/adewg/ICAR/blob/v1.4.1/types/icarDeviceReferenceType.json

Does Birth Event allow for duplication of data? animalDetail field
implementation of complex types in search
implementation of searching in arrays

Improve list handling in object checking tests


### Changes to ADE ###

icarInventoryTransactionType -> BaseModel to avoid circular import
icarDateTimeType -> PastDatetime
icarDateType -> PastDatetime (bson does not support date objects)
HeatEvent expirationDate -> FutureDatetime
icarRationIdType -> inherits from icarIdentifierType

### ADE Issues ###

An icarMedicineResource can be created empty
icarFeedStorageResource feedId is not of type icarFeedIdentifierType (which it is in icarFeedsInRationType, for example)
active and isActive used in different resources
