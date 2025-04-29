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
