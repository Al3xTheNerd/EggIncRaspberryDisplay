from decimal import Decimal
from math import floor, log

def formatArtifactTier(level):
    match level:
        case "INFERIOR":
            return "T1"
        case "LESSER":
            return "T2"
        case "NORMAL":
            return "T3"
        case "GREATER":
            return "T4"
        case _:
            return "T?"

units = [
       "",
       "k",
       "m",
       "b",
       "T",
       "q",
       "Q",
       "s",
       "S",
       "o",
       "N",
       "d",
       "U",
       "D",
       "Td",
       "qd",
       "Qd",
       "sd",
       "Sd",
       "Od",
       "Nd",
       "V",
       "uV",
       "dV",
       "tV",
       "qV",
       "sV",
       "SV",
       "OV",
       "NV",
       "tT"
    ]
role_units = [
       "Farmer",
       "Farmer",
       "Farmer",
       "Farmer",
       "Farmer II",
       "Farmer III",
       "Kilofarmer",
       "Kilofarmer II",
       "Kilofarmer III",
       "Megafarmer",
       "Megafarmer II",
       "Megafarmer III",
       "Gigafarmer",
       "Gigafarmer II",
       "Gigafarmer III",
       "Terafarmer",
       "Terafarmer II",
       "Terafarmer III",
       "Petafarmer",
       "Petafarmer II",
       "Petafarmer III",
       "Exafarmer",
       "Exafarmer II",
       "Exafarmer III",
       "Zettafarmer",
       "Zettafarmer II",
       "Zettafarmer III",
       "Yottafarmer",
       "Yottafarmer II",
       "Yottafarmer III",
       "Xennafarmer",
       "Xennafarmer II",
       "Xennafarmer III",
       "Weccafarmer",
       "Weccafarmer II",
       "Weccafarmer III",
       "Vendafarmer",
       "Vendafarmer II",
       "Vendafarmer III",
       "Uadafarmer",
       "Uadafarmer II",
       "Uadafarmer III",
       "Treidafarmer",
       "Treidafarmer II",
       "Treidafarmer III",
       "Quadafarmer",
       "Quadafarmer II",
       "Quadafarmer III",
       "Pendafarmer",
       "Pendafarmer II",
       "Pendafarmer III",
       "Exedafarmer",
       "Exedafarmer II",
       "Exedafarmer III"
    ]


def get_earning_bonus_data(backup):
    """Pull all relavent EB data from backup"""
    backup = backup["backup"]
    researchList = backup["game"]["epicResearch"]
    soulFood = 0
    prophecyBonus = 0
    for research in researchList:
        if research["id"] == "soul_eggs":
            soulFood = research["level"]
        if research["id"] == "prophecy_bonus":
            prophecyBonus = research["level"]
    prophecyEggs = backup["game"]["eggsOfProphecy"]
    soulEggs = backup["game"]["soulEggsD"]
    
    returndict = {
        "sF" : soulFood,
        "pB" : prophecyBonus,
        "sE" : soulEggs,
        "pE" : prophecyEggs
    }
    return returndict

def human_format(number: Decimal):
    k = Decimal(1000.0)
    magnitude = int(floor(log(number, k)))
    return '%.3f%s' % (number / k**magnitude, units[magnitude])

def calculate_earning_bonus(soulEggs: Decimal, prophecyEggs: Decimal, prophecyBonus: Decimal, soulFood: Decimal, human: bool):
    try:
        prophecyEggBonus = (Decimal(1) + Decimal(0.05) + (Decimal(0.01) * Decimal(prophecyBonus)))**Decimal(prophecyEggs) * (Decimal(10) + Decimal(soulFood))
        EB = Decimal(prophecyEggBonus) * Decimal(soulEggs)
        if human == True:
            EB = human_format(EB)
        return EB
    except:
        return False

def get_order_of_magnitude_rank(eb: Decimal):
    magnitude = len(str(round(eb)))
    if magnitude >= 55:
        return 'Infinifarmer'
    return role_units[magnitude]
