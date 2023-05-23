#translator_search

#dictionary taking shorthand stat names and full backend stat names
translates = {
    "dmg":"base damage / melee damage",
    "cc":"critical chance",
    "cd":"critical damage",
    "as":"fire rate / attack speed",
    "fr":"fire rate / attack speed",
    "ic":"channeling damage",
    "rec":"recoil",
    "ms":"multishot",
    "tox":"toxin damage",
    "cold":"cold damage",
    "elec":"electric damage",
    "heat":"heat damage",
    "slide":"critical chance on slide attack",
    "fin":"finisher damage",
    "dtg":"damage vs grineer",
    "dti":"damage vs infested",
    "dtc":"damage vs corpus",
    "ammo":"ammo maximum",
    "imp":"impact damage",
    "punc":"puncture damage",
    "slash":"slash damage",
    "mag":"magazine capacity",
    "pt":"punch through",
    "sc":"status chance",
    "r":"range",
    "sd":"status duration",
    "eff":"channeling efficiency",
    "rls":"reload speed",
    "pfs":"projectile speed",
    "z":"zoom"
}

def translate(stat):
    if stat in translates:
        stat_name = translates.get(stat).lower()
        return stat_name
    else:
        return stat