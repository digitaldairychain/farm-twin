"""
Collection of enums used in ICAR data standards.

See here for more details: https://github.com/adewg/ICAR/tree/ADE-1/enums
"""
from enum import Enum


class icarAnimalSpecieType(str, Enum):
    buffalo = "Buffalo"
    cattle = "Cattle"
    deer = "Deer"
    elk = "Elk"
    goat = "Goat"
    horse = "Horse"
    pig = "Pig"
    sheep = "Sheep"


class icarAnimalGenderType(str, Enum):
    female = "Female",
    femaleNeuter = "FemaleNeuter"
    Freemartin = "Freemartin"
    male = "Male"
    maleCryptorchid = "MaleCryptorchid"
    maleNeuter = "MaleNeuter"
    unknown = "Unknown"


class icarProductionPurposeType(str, Enum):
    meat = "Meat"
    milk = "Milk"
    wool = "Wool"


class icarAnimalStatusType(str, Enum):
    alive = "Alive"
    dead = "Dead"
    offFarm = "OffFarm"
    unknown = "Unknown"


class icarAnimalReproductionStatusType(str, Enum):
    open = "Open"
    inseminated = "Inseminated"
    pregnant = "Pregnant"
    notPregnant = "NotPregnant"
    birthed = "Birthed"
    doNotBreed = "DoNotBreed"
    pregnantMultipleFoetus = "PregnantMultipleFoetus"


class icarAnimalLactationStatusType(str, Enum):
    dry = "Dry"
    lead = "Lead"
    fresh = "Fresh"
    early = "Early"
    lactating = "Lactating"


class icarAnimalHealthStatusType(str, Enum):
    healthy = "Healthy"
    suspicious = "Suspicious"
    ill = "Ill"
    inTreatment = "InTreatment"
    toBeCulled = "ToBeCulled"


class uncefactMassUnitsType(str, Enum):
    kgm = "KGM",
    grm = "GRM",
    lbr = "LBR",
    tne = "TNE",
    mc = "MC",
    mgm = "MGM",
    onz = "ONZ",
    pn = "PN"


class icarWeightMethodType(str, Enum):
    loadCell = "LoadCell",
    girth = "Girth",
    assessed = "Assessed",
    walkover = "WalkOver",
    predicted = "Predicted",
    imaged = "Imaged",
    frontEndCorrelated = "FrontEndCorrelated",
    groupAverage = "GroupAverage"


class icarAggregationType(str, Enum):
    average = "Average",
    sum = "Sum",
    stDev = "StDev",
    min = "Min",
    max = "Max",
    count = "Count"


class uncefactTimeUnitsType(str, Enum):
    sec = "SEC",
    min = "MIN"


class icarMessageType(str, Enum):
    milkingVisits = "MilkingVisits",
    testDayResults = "TestDayResults",
    births = "Births",
    deaths = "Deaths",
    arrivals = "Arrivals",
    departures = "Departures",
    animals = "Animals",
    pregnancy = "PregnancyChecks",
    heats = "Heats",
    dryingOffs = "DryingOffs",
    inseminations = "Inseminations",
    abortions = "Abortions",
    parturitions = "Parturitions",
    matingRecommendations = "MatingRecommendations",
    devices = "Devices",
    weights = "Weights",
    locations = "Locations",
    animalSetJoins = "AnimalSetJoins",
    animalSetLeaves = "AnimalSetLeaves",
    progenyDetails = "ProgenyDetails",
    breedingValues = "BreedingValues",
    feedIntakes = "FeedIntakes",
    feedReports = "FeedReports",
    feedRecommendations = "FeedRecommendations",
    rations = "Rations",
    feedStorages = "FeedStorages",
    gestations = "Gestations",
    doNotBreedInstructions = "DoNotBreedInstructions",
    reproductionStatusObservation = "ReproductionStatusObservations",
    lactations = "Lactations",
    lactationStatusObservations = "LactationStatusObservations",
    withdrawals = "Withdrawals",
    dailyMilkingAverages = "DailyMilkingAverages",
    diagnoses = "Diagnoses",
    treatments = "Treatments",
    treatmentPrograms = "TreatmentPrograms",
    healthStatusObservations = "HealthStatusObservations",
    conformationScores = "ConformationScores",
    typeClassifications = "TypeClassifications",
    statistics = "Statistics",
    schemes = "Schemes",
    embryos = "Embryos",
    semenStraws = "SemenStraws",
    flushings = "Flushings",
    groupTreatments = "GroupTreatments",
    groupBirths = "GroupBirths",
    groupArrivals = "GroupArrivals",
    groupDepartures = "GroupDepartures",
    groupDeaths = "GroupDeaths",
    groupWeights = "GroupWeights",
    other = "Other"


class icarWithdrawalProductType(str, Enum):
    meat = "Meat",
    milk = "Milk",
    eggs = "Eggs",
    honey = "Honey",
    velvet = "Velvet",
    fibre = "Fibre",
    other = "Other"
