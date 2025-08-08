"""
Collection of enums used in ICAR data standards.
See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/enums
"""

from enum import Enum


class icarFeedDurationTypeUnitCode(str, Enum):
    _sec = ("SEC",)
    _min = ("MIN",)


class icarAnimalLactationStatusType(str, Enum):
    _dry = ("Dry",)
    _lead = ("Lead",)
    _fresh = ("Fresh",)
    _early = ("Early",)
    _lactating = "Lactating"


class icarDeathMethodType(str, Enum):
    _perished = ("Perished",)
    _slaughter = ("Slaughter",)
    _culled = ("Culled",)
    _theft = ("Theft",)
    _lost = ("Lost",)
    _accident = ("Accident",)
    _other = "Other"


class icarMilkingRemarksType(str, Enum):
    _animalSick = ("AnimalSick",)
    _milkingIncomplete = ("MilkingIncomplete",)
    _teatSeparated = ("TeatSeparated",)
    _milkedSeparately = ("MilkedSeparately",)
    _samplingFailed = "SamplingFailed"


class icarReproCalvingEaseType(str, Enum):
    _easyUnassisted = ("EasyUnassisted",)
    _easyAssisted = ("EasyAssisted",)
    _difficultExtraAssistance = ("DifficultExtraAssistance",)
    _difficultVeterinaryCare = ("DifficultVeterinaryCare",)
    _caesareanOrSurgery = "CaesareanOrSurgery"


class icarAnimalReproductionStatusType(str, Enum):
    _open = ("Open",)
    _inseminated = ("Inseminated",)
    _pregnant = ("Pregnant",)
    _notPregnant = ("NotPregnant",)
    _birthed = ("Birthed",)
    _doNotBreed = ("DoNotBreed",)
    _pregnantMultipleFoetus = "PregnantMultipleFoetus"


class icarAnimalRelationType(str, Enum):
    _genetic = ("Genetic",)
    _recipient = ("Recipient",)
    _adoptive = "Adoptive"


class icarDepartureReasonType(str, Enum):
    _age = ("Age",)
    _superfluous = ("Superfluous",)
    _slaughter = ("Slaughter",)
    _sale = ("Sale",)
    _newborn = ("Newborn",)
    _legOrClaw = ("LegOrClaw",)
    _nutrition = ("Nutrition",)
    _parturition = ("Parturition",)
    _mastitis = ("Mastitis",)
    _fertility = ("Fertility",)
    _health = ("Health",)
    _production = ("Production",)
    _milkingAbility = ("MilkingAbility",)
    _badType = ("BadType",)
    _behaviour = ("Behaviour",)
    _other = ("Other",)
    _unknown = "Unknown"


class icarProductFamilyType(str, Enum):
    _animalFeeds = ("Animal Feeds",)
    _animalReproductiveProducts = ("Animal Reproductive Products",)
    _veterinarySupplies = ("Veterinary Supplies",)
    _seedandPlantMaterial = ("Seed and Plant Material",)
    _fertilisersandNutrients = ("Fertilisers and Nutrients",)
    _pestControlProducts = ("Pest Control Products",)
    _otherAnimalProducts = ("Other Animal Products",)
    _milkingSupplies = ("Milking Supplies",)
    _fencingSupplies = ("Fencing Supplies",)
    _waterSystemSupplies = ("Water System Supplies",)
    _fuel = ("Fuel",)
    _other = "Other"


class icarRegistrationReasonType(str, Enum):
    _born = ("Born",)
    _registered = "Registered"


class icarReproSemenPreservationType(str, Enum):
    _liquid = ("Liquid",)
    _frozen = "Frozen"


class icarParturitionBirthSizeType(str, Enum):
    _extraSmall = ("ExtraSmall",)
    _small = ("Small",)
    _average = ("Average",)
    _large = ("Large",)
    _extraLarge = "ExtraLarge"


class icarMilkingsPerDayType(str, Enum):
    _1 = ("1",)
    _2 = ("2",)
    _3 = ("3",)
    _4 = ("4",)
    _robot = "Robot"


class uncefactDoseUnitsType(str, Enum):
    _MLT = ("MLT",)
    _LTR = ("LTR",)
    _MGM = ("MGM",)
    _GRM = ("GRM",)
    _XTU = ("XTU",)
    _XVI = ("XVI",)
    _XAR = ("XAR",)
    _XCQ = ("XCQ",)
    _GJ = ("GJ",)
    _GL = ("GL",)
    _GRN = ("GRN",)
    _L19 = ("L19",)
    _NA = ("NA",)
    _SYR = ("SYR",)
    _WW = "WW"


class icarMilkSamplingSchemeType(str, Enum):
    _proportionalSizeSamplingOfAllMilkings = ("ProportionalSizeSamplingOfAllMilkings",)
    _constantSizeSamplingOfAllMilkings = ("ConstantSizeSamplingOfAllMilkings",)
    _alternateSampling = ("AlternateSampling",)
    _correctedSampling = ("CorrectedSampling",)
    _oneMilkingSampleInAMS = ("OneMilkingSampleInAMS",)
    _mulitpleMilkingSampleInAMS = "MulitpleMilkingSampleInAMS"


class icarAttentionPriorityType(str, Enum):
    _informational = ("Informational",)
    _normal = ("Normal",)
    _urgent = ("Urgent",)
    _critical = "Critical"


class icarAnimalIdSchemeCode(str, Enum):
    _nl_ubn = ("nl.ubn",)
    _be_pen = ("be.pen",)
    _gb_rpa = ("gb.rpa",)
    _ni_daera = "ni.daera"


class icarReproHeatSignType(str, Enum):
    _slime = ("Slime",)
    _clearSlime = ("ClearSlime",)
    _interestedInOtherAnimals = ("InterestedInOtherAnimals",)
    _bawling = ("Bawling",)
    _blood = ("Blood",)
    _standsUnder = "StandsUnder"


class icarConformationTraitType(str, Enum):
    _angularity = ("Angularity",)
    _backLength = ("BackLength",)
    _backWidth = ("BackWidth",)
    _bodyConditionScore = ("BodyConditionScore",)
    _bodyDepth = ("BodyDepth",)
    _bodyLength = ("BodyLength",)
    _boneStructure = ("BoneStructure",)
    _centralLigament = ("CentralLigament",)
    _chestDepth = ("ChestDepth",)
    _chestWidth = ("ChestWidth",)
    _clawAngle = ("ClawAngle",)
    _dairyStrength = ("DairyStrength",)
    _feetLegs = ("FeetLegs",)
    _finalScore = ("FinalScore",)
    _flankDepth = ("FlankDepth",)
    _footAngle = ("FootAngle",)
    _forePasternsSideView = ("ForePasternsSideView",)
    _foreUdderAttachment = ("ForeUdderAttachment",)
    _foreUdderLength = ("ForeUdderLength",)
    _frame = ("Frame",)
    _frontLegsFrontView = ("FrontLegsFrontView",)
    _frontTeatPlacement = ("FrontTeatPlacement",)
    _heightAtRump = ("HeightAtRump",)
    _heightAtWithers = ("HeightAtWithers",)
    _hindPasternsSideView = ("HindPasternsSideView",)
    _hockDevelopment = ("HockDevelopment",)
    _lengthOfRump = ("LengthOfRump",)
    _locomotion = ("Locomotion",)
    _loinStrength = ("LoinStrength",)
    _muscularity = ("Muscularity",)
    _muscularityComposite = ("MuscularityComposite",)
    _muscularityShoulderSideView = ("MuscularityShoulderSideView",)
    _muscularityShoulderTopView = ("MuscularityShoulderTopView",)
    _muzzleWidth = ("MuzzleWidth",)
    _rearLegsRearView = ("RearLegsRearView",)
    _rearLegsSet = ("RearLegsSet",)
    _rearLegsSideView = ("RearLegsSideView",)
    _rearTeatPlacement = ("RearTeatPlacement",)
    _rearUdderHeight = ("RearUdderHeight",)
    _rearUdderWidth = ("RearUdderWidth",)
    _roundingOfRibs = ("RoundingOfRibs",)
    _rumpAngle = ("RumpAngle",)
    _rumpLength = ("RumpLength",)
    _rumpWidth = ("RumpWidth",)
    _skinThickness = ("SkinThickness",)
    _stature = ("Stature",)
    _tailSet = ("TailSet",)
    _teatDirection = ("TeatDirection",)
    _teatForm = ("TeatForm",)
    _teatLength = ("TeatLength",)
    _teatPlacementRearView = ("TeatPlacementRearView",)
    _teatPlacementSideView = ("TeatPlacementSideView",)
    _teatThickness = ("TeatThickness",)
    _thicknessOfBone = ("ThicknessOfBone",)
    _thicknessOfTeat = ("ThicknessOfTeat",)
    _thicknessOfLoin = ("ThicknessOfLoin",)
    _thighLength = ("ThighLength",)
    _thighRoundingSideView = ("ThighRoundingSideView",)
    _thighWidthRearView = ("ThighWidthRearView",)
    _thurlWidth = ("ThurlWidth",)
    _topLine = ("TopLine",)
    _type = ("Type",)
    _udder = ("Udder",)
    _udderBalance = ("UdderBalance",)
    _udderDepth = ("UdderDepth",)
    _widthAtHips = ("WidthAtHips",)
    _widthAtPins = "WidthAtPins"


class icarRecommendationType(str, Enum):
    _sireRecommended = ("SireRecommended",)
    _recommendationImpossible = ("RecommendationImpossible",)
    _beefSire = ("BeefSire",)
    _noBreedingSire = "NoBreedingSire"


class icarDepartureKindType(str, Enum):
    _internalTransfer = ("InternalTransfer",)
    _export = ("Export",)
    _slaughter = ("Slaughter",)
    _newborn = ("Newborn",)
    _studService = ("StudService",)
    _studServiceReturn = ("StudServiceReturn",)
    _agistment = ("Agistment",)
    _agistmentReturn = ("AgistmentReturn",)
    _show = ("Show",)
    _showReturn = ("ShowReturn",)
    _sale = ("Sale",)
    _saleReturn = ("SaleReturn",)
    _other = "Other"


class icarReproHeatCertaintyType(str, Enum):
    _inHeat = ("InHeat",)
    _suspect = ("Suspect",)
    _potential = "Potential"


class icarMilkingType(str, Enum):
    _officialMilkResultSuppliedByMRO = ("OfficialMilkResultSuppliedByMRO",)
    _measureByICARApprovedEquipment = ("MeasureByICARApprovedEquipment",)
    _measureByNotApprovedEquipment = "MeasureByNotApprovedEquipment"


class icarDeathDisposalMethodType(str, Enum):
    _approvedService = ("ApprovedService",)
    _consumption = ("Consumption",)
    _onPremise = ("OnPremise",)
    _other = "Other"


class icarProductionPurposeType(str, Enum):
    _meat = ("Meat",)
    _milk = ("Milk",)
    _wool = "Wool"


class icarMilkSamplingMomentType(str, Enum):
    _composite = ("Composite",)
    _morning = ("Morning",)
    _evening = "Evening"


class icarCarcassSideType(str, Enum):
    _left = ("Left",)
    _right = ("Right",)
    _both = "Both"


class icarConformationScoringMethodType(str, Enum):
    _manual = ("Manual",)
    _automated = "Automated"


class icarInventoryTransactionKindType(str, Enum):
    _receipt = ("Receipt",)
    _disposal = ("Disposal",)
    _onHand = ("OnHand",)
    _produce = ("Produce",)
    _stockTake = ("StockTake",)
    _use = "Use"


class icarAnimalSpecieType(str, Enum):
    _buffalo = ("Buffalo",)
    _cattle = ("Cattle",)
    _deer = ("Deer",)
    _elk = ("Elk",)
    _goat = ("Goat",)
    _horse = ("Horse",)
    _pig = ("Pig",)
    _sheep = "Sheep"


class icarParturitionBirthStatusType(str, Enum):
    _alive = ("Alive",)
    _stillborn = ("Stillborn",)
    _aborted = ("Aborted",)
    _diedBeforeTaggingDate = ("DiedBeforeTaggingDate",)
    _diedAfterTaggingDate = ("DiedAfterTaggingDate",)
    _slaughteredAtBirth = ("SlaughteredAtBirth",)
    _euthanisedAtBirth = "EuthanisedAtBirth"


class icarMilkCharacteristicCodeType(str, Enum):
    _SCC = ("SCC",)
    _FAT = ("FAT",)
    _PROTEIN = ("PROTEIN",)
    _LAC = ("LAC",)
    _UREA = ("UREA",)
    _BLOOD = ("BLOOD",)
    _ACETONE = ("ACETONE",)
    _BHB = ("BHB",)
    _LDH = ("LDH",)
    _PRO = ("PRO",)
    _AVGCOND = ("AVGCOND",)
    _MAXCOND = ("MAXCOND",)
    _AVGFLWR = ("AVGFLWR",)
    _MAXFLWR = ("MAXFLWR",)
    _WEIGHT = ("WEIGHT",)
    _TEMPERATURE = "TEMPERATURE"


class icarMethodType(str, Enum):
    _analyzed = ("Analyzed",)
    _derived = "Derived"


class icarValidSampleFillingIndicatorType(str, Enum):
    _0 = ("0",)
    _1 = ("1",)
    _2 = "2"


class icarWeightMethodType(str, Enum):
    _loadCell = ("LoadCell",)
    _girth = ("Girth",)
    _assessed = ("Assessed",)
    _walkOver = ("WalkOver",)
    _predicted = ("Predicted",)
    _imaged = ("Imaged",)
    _frontEndCorrelated = ("FrontEndCorrelated",)
    _groupAverage = "GroupAverage"


class uncefactMassUnitsType(str, Enum):
    _KGM = ("KGM",)
    _GRM = ("GRM",)
    _LBR = ("LBR",)
    _TNE = ("TNE",)
    _MC = ("MC",)
    _MGM = ("MGM",)
    _ONZ = ("ONZ",)
    _PN = "PN"


class icarPositionOnAnimalType(str, Enum):
    _legsFrontLeft = ("LegsFrontLeft",)
    _legsFrontRight = ("LegsFrontRight",)
    _legsRearLeft = ("LegsRearLeft",)
    _legsRearRight = ("LegsRearRight",)
    _udderFrontLeft = ("UdderFrontLeft",)
    _udderFrontRight = ("UdderFrontRight",)
    _udderRearLeft = ("UdderRearLeft",)
    _udderRearRight = ("UdderRearRight",)
    _ovariesLeft = ("OvariesLeft",)
    _ovariesRight = ("OvariesRight",)
    _ovariesUnknown = ("OvariesUnknown",)
    _neck = ("Neck",)
    _head = ("Head",)
    _mouth = ("Mouth",)
    _back = ("Back",)
    _testes = ("Testes",)
    _other = "Other"


class icarArrivalReasonType(str, Enum):
    _purchase = ("Purchase",)
    _internalTransfer = ("InternalTransfer",)
    _imported = ("Imported",)
    _studService = ("StudService",)
    _studServiceReturn = ("StudServiceReturn",)
    _slaughter = ("Slaughter",)
    _agistment = ("Agistment",)
    _agistmentReturn = ("AgistmentReturn",)
    _show = ("Show",)
    _showReturn = ("ShowReturn",)
    _sale = ("Sale",)
    _saleReturn = ("SaleReturn",)
    _other = "Other"


class icarDiagnosisSeverityType(str, Enum):
    _light = ("Light",)
    _moderate = ("Moderate",)
    _severe = "Severe"


class icarWithdrawalProductType(str, Enum):
    _meat = ("Meat",)
    _milk = ("Milk",)
    _eggs = ("Eggs",)
    _honey = ("Honey",)
    _velvet = ("Velvet",)
    _fibre = ("Fibre",)
    _other = "Other"


class icarAnimalStatusType(str, Enum):
    _alive = ("Alive",)
    _dead = ("Dead",)
    _offFarm = ("OffFarm",)
    _unknown = "Unknown"


class icarConformationTraitGroupType(str, Enum):
    _composite = ("Composite",)
    _linear = "Linear"


class icarMilkingTypeCode(str, Enum):
    _manual = ("Manual",)
    _automated = "Automated"


class icarReproPregnancyResultType(str, Enum):
    _empty = ("Empty",)
    _pregnant = ("Pregnant",)
    _multiple = ("Multiple",)
    _unknown = "Unknown"


class icarMilkRecordingSchemeType(str, Enum):
    _allMilkingsAtTestday = ("AllMilkingsAtTestday",)
    _allMilkingsInPeriod = ("AllMilkingsInPeriod",)
    _oneMilkingAtTestday = "OneMilkingAtTestday"


class icarFeedCategoryType(str, Enum):
    _concentrate = ("Concentrate",)
    _roughage = ("Roughage",)
    _additives = ("Additives",)
    _other = "Other"


class icarAttentionCauseType(str, Enum):
    _activity = ("Activity",)
    _animalTemperature = ("AnimalTemperature",)
    _bodyCondition = ("BodyCondition",)
    _eatingLess = ("EatingLess",)
    _environmentTemperature = ("EnvironmentTemperature",)
    _disturbance = ("Disturbance",)
    _health = ("Health",)
    _heartRate = ("HeartRate",)
    _inactivity = ("Inactivity",)
    _ketosis = ("Ketosis",)
    _lameness = ("Lameness",)
    _location = ("Location",)
    _lowerRumination = ("LowerRumination",)
    _lyingTooLong = ("LyingTooLong",)
    _lyingTooShort = ("LyingTooShort",)
    _mastitis = ("Mastitis",)
    _mobilityScore = ("MobilityScore",)
    _noMovement = ("NoMovement",)
    _parturition = ("Parturition",)
    _postParturitionRisk = ("PostParturitionRisk",)
    _prolongedParturition = ("ProlongedParturition",)
    _respirationRate = ("RespirationRate",)
    _standing = ("Standing",)
    _standingUp = ("StandingUp",)
    _walking = ("Walking",)
    _heat = ("Heat",)
    _lowBattery = ("LowBattery",)
    _offline = ("Offline",)
    _underWeight = ("UnderWeight",)
    _overWeight = ("OverWeight",)
    _atTargetWeight = ("AtTargetWeight",)
    _other = ("Other",)
    _undefined = "Undefined"


class icarGroupEventMethodType(str, Enum):
    _existingAnimalSet = ("ExistingAnimalSet",)
    _embeddedAnimalSet = ("EmbeddedAnimalSet",)
    _inventoryClassification = ("InventoryClassification",)
    _embeddedAnimalSetAndInventoryClassification = (
        "EmbeddedAnimalSetAndInventoryClassification"
    )


class icarStatisticsPurposeType(str, Enum):
    _testDay = ("TestDay",)
    _feeding = ("Feeding",)
    _reproduction = ("Reproduction",)
    _breedingValues = ("BreedingValues",)
    _typeClassification = ("TypeClassification",)
    _registration = "Registration"


class icarObservationStatusType(str, Enum):
    _measured = ("Measured",)
    _notMeasured = ("NotMeasured",)
    _calculated = ("Calculated",)
    _notCalculated = "NotCalculated"


class icarAnimalGenderType(str, Enum):
    _female = ("Female",)
    _femaleNeuter = ("FemaleNeuter",)
    _freemartin = ("Freemartin",)
    _male = ("Male",)
    _maleCryptorchid = ("MaleCryptorchid",)
    _maleNeuter = ("MaleNeuter",)
    _unknown = "Unknown"


class icarReproHeatIntensityType(str, Enum):
    _veryWeak = ("VeryWeak",)
    _weak = ("Weak",)
    _normal = ("Normal",)
    _strong = ("Strong",)
    _veryStrong = "VeryStrong"


class icarBottleIdentifierType(str, Enum):
    _BRC = ("BRC",)
    _RFD = "RFD"


class icarDiagnosisStageType(str, Enum):
    _early = ("Early",)
    _acute = ("Acute",)
    _subAcute = ("SubAcute",)
    _chronic = ("Chronic",)
    _acuteOnChronic = ("AcuteOnChronic",)
    _endStage = ("EndStage",)
    _other = "Other"


class icarAttentionCategoryType(str, Enum):
    _behaviour = ("Behaviour",)
    _environment = ("Environment",)
    _health = ("Health",)
    _reproduction = ("Reproduction",)
    _deviceIssue = ("DeviceIssue",)
    _weight = ("Weight",)
    _other = "Other"


class icarReproHeatDetectionMethodType(str, Enum):
    _chemical = ("Chemical",)
    _visual = ("Visual",)
    _pedometer = ("Pedometer",)
    _collar = ("Collar",)
    _earTag = ("EarTag",)
    _bolus = ("Bolus",)
    _other = "Other"


class icarGroupType(str, Enum):
    _herd = ("Herd",)
    _lactationNumber = ("LactationNumber",)
    _daysInMilk = ("DaysInMilk",)
    _animalSet = "AnimalSet"


class icarCarcassPrimalType(str, Enum):
    _total = ("Total",)
    _forequarter = ("Forequarter",)
    _middle = ("Middle",)
    _hindquarter = "Hindquarter"


class icarChainProcessType(str, Enum):
    _anteMortem = ("AnteMortem",)
    _postMortem = "PostMortem"


class icarBatchResultSeverityType(str, Enum):
    _information = ("Information",)
    _warning = ("Warning",)
    _error = "Error"


class icarMilkRecordingProtocolType(str, Enum):
    _a_OfficialMRORepresentative = ("A-OfficialMRORepresentative",)
    _b_HerdOwnerOrNominee = ("B-HerdOwnerOrNominee",)
    _c_Both = "C-Both"


class icarReproInseminationType(str, Enum):
    _naturalService = ("NaturalService",)
    _runWithBull = ("RunWithBull",)
    _insemination = ("Insemination",)
    _implantation = "Implantation"


class icarDeathReasonType(str, Enum):
    _missing = ("Missing",)
    _parturition = ("Parturition",)
    _disease = ("Disease",)
    _accident = ("Accident",)
    _consumption = ("Consumption",)
    _culled = ("Culled",)
    _other = ("Other",)
    _unknown = ("Unknown",)
    _age = ("Age",)
    _mastitis = ("Mastitis",)
    _production = ("Production",)
    _legOrClaw = ("LegOrClaw",)
    _milkingAbility = ("MilkingAbility",)
    _nutrition = ("Nutrition",)
    _fertility = "Fertility"


class icarReproEmbryoFlushingMethodType(str, Enum):
    _OPU_IVF = ("OPU-IVF",)
    _superovulation = "Superovulation"


class icarMessageType(str, Enum):
    _milkingVisits = ("MilkingVisits",)
    _testDayResults = ("TestDayResults",)
    _births = ("Births",)
    _deaths = ("Deaths",)
    _arrivals = ("Arrivals",)
    _departures = ("Departures",)
    _animals = ("Animals",)
    _pregnancyChecks = ("PregnancyChecks",)
    _heats = ("Heats",)
    _dryingOffs = ("DryingOffs",)
    _inseminations = ("Inseminations",)
    _abortions = ("Abortions",)
    _parturitions = ("Parturitions",)
    _matingRecommendations = ("MatingRecommendations",)
    _devices = ("Devices",)
    _weights = ("Weights",)
    _locations = ("Locations",)
    _animalSetJoins = ("AnimalSetJoins",)
    _animalSetLeaves = ("AnimalSetLeaves",)
    _progenyDetails = ("ProgenyDetails",)
    _breedingValues = ("BreedingValues",)
    _feedIntakes = ("FeedIntakes",)
    _feedReports = ("FeedReports",)
    _feedRecommendations = ("FeedRecommendations",)
    _rations = ("Rations",)
    _feedStorages = ("FeedStorages",)
    _gestations = ("Gestations",)
    _doNotBreedInstructions = ("DoNotBreedInstructions",)
    _reproductionStatusObservations = ("ReproductionStatusObservations",)
    _lactations = ("Lactations",)
    _lactationStatusObservations = ("LactationStatusObservations",)
    _withdrawals = ("Withdrawals",)
    _dailyMilkingAverages = ("DailyMilkingAverages",)
    _diagnoses = ("Diagnoses",)
    _treatments = ("Treatments",)
    _treatmentPrograms = ("TreatmentPrograms",)
    _healthStatusObservations = ("HealthStatusObservations",)
    _conformationScores = ("ConformationScores",)
    _typeClassifications = ("TypeClassifications",)
    _statistics = ("Statistics",)
    _schemes = ("Schemes",)
    _embryos = ("Embryos",)
    _semenStraws = ("SemenStraws",)
    _flushings = ("Flushings",)
    _groupTreatments = ("GroupTreatments",)
    _groupBirths = ("GroupBirths",)
    _groupArrivals = ("GroupArrivals",)
    _groupDepartures = ("GroupDepartures",)
    _groupDeaths = ("GroupDeaths",)
    _groupWeights = ("GroupWeights",)
    _other = "Other"


class icarAnimalHealthStatusType(str, Enum):
    _healthy = ("Healthy",)
    _suspicious = ("Suspicious",)
    _ill = ("Ill",)
    _inTreatment = ("InTreatment",)
    _toBeCulled = "ToBeCulled"


class icarSetPurposeType(str, Enum):
    _enclosure = ("Enclosure",)
    _feeding = ("Feeding",)
    _finishing = ("Finishing",)
    _growing = ("Growing",)
    _health = ("Health",)
    _lactation = ("Lactation",)
    _movement = ("Movement",)
    _rearing = ("Rearing",)
    _reproduction = ("Reproduction",)
    _session = ("Session",)
    _other = "Other"


class icarReproPregnancyMethodType(str, Enum):
    _echography = ("Echography",)
    _palpation = ("Palpation",)
    _blood = ("Blood",)
    _milk = ("Milk",)
    _visual = ("Visual",)
    _other = "Other"


class icarLactationType(str, Enum):
    _normal = ("Normal",)
    _100Days = ("100Days",)
    _200Days = ("200Days",)
    _305Days = ("305Days",)
    _365Days = "365Days"


class icarTestDayCodeType(str, Enum):
    _dry = ("Dry",)
    _samplingImpossible = ("SamplingImpossible",)
    _sick = "Sick"


class icarBreedingValueCalculationType(str, Enum):
    _breedingValue = ("BreedingValue",)
    _parentAverageBreedingValue = ("ParentAverageBreedingValue",)
    _genomicBreedingValue = ("GenomicBreedingValue",)
    _convertedBreedingValue = ("ConvertedBreedingValue",)
    _other = "Other"


class icarAggregationType(str, Enum):
    _average = ("Average",)
    _sum = ("Sum",)
    _stDev = ("StDev",)
    _min = ("Min",)
    _max = ("Max",)
    _count = "Count"


class icarCarcassStateType(str, Enum):
    _hot = ("Hot",)
    _cold = "Cold"
