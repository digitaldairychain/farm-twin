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
