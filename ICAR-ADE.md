# { farm-twin } ICAR ADE Integration Status #

{ farm-twin } aligns with v1.5.0 of the [ICAR Animal Data Exchange Standard](https://github.com/adewg/ICAR/blob/v1.5.0).

However, this is currently not a full implementation. The following sections document the [resource entities](https://github.com/adewg/ICAR/wiki/Resource-entities) that are implemented. 

Following that, we outline any changes that have been made to the specification and noted issues. 

## Resources ##

- [x] icarAnimalCoreResource
- [ ] icarAnimalSetResource
- [x] icarDeviceResource
- [x] icarFeedResource
- [x] icarFeedStorageResource
- [x] icarLocationResource
- [x] icarMedicineResource
- [x] icarRationResource
- [x] icarReproEmbryoResource
- [x] icarReproSemenStrawResource
- [ ] icarStatisticsResource

## Events ##

- [x] icarMovementArrivalEventResource
- [x] icarMovementBirthEventResource
- [x] icarMovementDeathEventResource
- [x] icarMovementDepartureEventResource
- [x] icarMilkingDryOffEventResource
- [x] icarMilkingVisitEventResource
- [x] icarTestDayResultEventResource
- [x] icarLactationStatusObservedEventResource
- [x] icarReproAbortionEventResource
- [x] icarReproDoNotBreedEventResource
- [x] icarReproHeatEventResource
- [x] icarReproInseminationEventResource
- [x] icarReproMatingRecommendationResource
- [x] icarReproParturitionEventResource
- [x] icarReproPregnancyCheckEventResource
- [x] icarReproStatusObservedEventResource
- [x] icarConformationScoreEventResource
- [x] icarWeightEventResource
- [x] icarGroupWeightEventResource
- [ ] icarAnimalSetJoinEventResource
- [ ] icarAnimalSetLeaveEventResource
- [ ] icarDiagnosisEventResource
- [x] icarTreatmentEventResource
- [ ] icarTreatmentProgramEventResource
- [ ] icarGroupTreatmentEventResource
- [x] icarFeedIntakeEventResource

## Summary Resources ##

- [ ] icarGestationResource
- [ ] icarLactationResource
- [ ] icarTestDayResource
- [ ] icarDailyMilkingAveragesResource
- [ ] icarBreedingValueResource
- [ ] icarFeedRecommendationResource
- [ ] icarFeedReportResource

## { farm-twin } changes to the ADE ###

- As per the working group [discussion](https://github.com/adewg/ICAR/discussions/485), { farm-twin } has made the 'meta' field required, and the 'source', 'sourceId' and 'modified' fields within that, also required.
- icarInventoryTransactionType -> BaseModel to avoid circular import
- icarDateTimeType -> PastDatetime (with some exceptions, where FutureDate is instead used)
- icarDateType -> PastDatetime (bson does not support date objects)
- icarReproHeatEventResource expirationDate -> FutureDatetime
- icarRationIdType -> inherits from icarIdentifierType

### ADE Issues ###

- icarMedicineResource can be created empty
- icarReproEmbryoResource can be created empty
- icarReproSemenStrawResource can be created empty
- icarFeedStorageResource feedId is not of type icarFeedIdentifierType (which it is in icarFeedsInRationType, for example)
- active and isActive field names are not used consistently
- A timestamp appears missing from some resources (such as icarConformationScoreEventResource) - do we rely on its creation date?
