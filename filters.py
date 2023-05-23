#filters

#wfm
filters = [
    ['critical chance','critical damage','fire rate / attack speed'],
    ['critical chance','critical damage','toxin damage'],
    ['fire rate / attack speed', 'critical damage', 'multishot'],
    ['fire rate / attack speed', 'critical chance', 'multishot'],
    ['critical chance', 'critical damage', 'multishot'],
    ['critical damage', 'fire rate / attack speed', 'range'],
    ['status chance','multishot','fire rate / attack speed'],
    ['base damage / melee damage', 'multishot', 'toxin damage'],
    ['base damage / melee damage', 'multishot', 'electric damage'],
    ['fire rate / attack speed', 'multishot', 'electric damage'],
    ['critical chance','heat damage','damage vs corpus'],
    ['critical chance','electric damage','damage vs corpus'],
    ['base damage / melee damage', 'multishot', 'critical damage'],
    ['base damage / melee damage', 'multishot', 'critical chance'],
    ['base damage / melee damage', 'critical damage', 'critical chance'],
    ['toxin damage', 'multishot', 'critical damage'],
    ['critical chance', 'critical damage', 'channeling damage'],
    ['base damage / melee damage', 'multishot', 'fire rate / attack speed'],
    ['base damage / melee damage', 'multishot', 'status chance'],
    ['critical damage', 'fire rate / attack speed', 'channeling efficiency'],
    ['critical damage', 'fire rate / attack speed', 'heat damage'],
    ['critical damage', 'multishot', 'status chance'],
    ['critical damage','slash damage','base damage / melee damage'],
    ['critical damage','multishot','punch_through']
]
neg_cc_filter_pos = [['fire rate / attack speed', 'toxin damage', 'multishot'],['base damage / melee damage', 'toxin damage', 'multishot'],['status chance','base damage / melee damage', 'multishot'],['multisht', 'fire rate / attack speed','status chance']]
neg_cc_filter_neg = ['critical chance','recoil','puncture damage','zoom','impact damage']
neg_cc_weapons = ['felarx','phenmor','laetum']

negative_filter = ['impact damage', 'puncture damage', 'recoil', 'ammo maximum', 'zoom', 'channeling efficiency', 'critical chance on slide attack', 'finisher damage', 'projectile speed']

#specific gun rolls
cedo_filters = [['fire rate / attack speed','toxin damage','multishot'],['toxin damage','fire rate / attack speed','critical damage']]
ogris_filters = [['base damage / melee damage', 'multishot','projectile speed'],['base damage / melee damage', 'multishot','fire rate / attack speed'],['base damage / melee damage', 'multishot','magazine capacity']]
tonkor_3 = ['magazine capacity','fire rate / attack speed','reload speed']
phantasma = [['base damage / melee damage', 'multishot', 'electric damage'],['fire rate / attack speed', 'multishot', 'electric damage']]
profit_taker = [['critical chance','heat damage','damage vs corpus'],['critical chance','electric damage','damage vs corpus']]

#specific weapon list
neg_mag_weapons = ['epitaph','dread','daikyu','nataruk','vectis','cernos','lenz','proboscis cernos','kuva bramma','mutalist cernos','paris','exergis','knell']

#gun rolls
gun_filters = [
    ['critical chance','critical damage','fire rate / attack speed'],
    ['critical chance','critical damage','toxin damage'],
    ['fire rate / attack speed', 'critical damage', 'multishot'],
    ['fire rate / attack speed', 'critical chance', 'multishot'],
    ['critical chance', 'critical damage', 'multishot'],
    ['status chance','multishot','fire rate / attack speed'],
    ['base damage / melee damage', 'multishot', 'toxin damage'],
    ['base damage / melee damage', 'multishot', 'critical damage'],
    ['base damage / melee damage', 'multishot', 'critical chance'],
    ['base damage / melee damage', 'critical damage', 'critical chance'],
    ['toxin damage', 'multishot', 'critical damage'],
    ['base damage / melee damage', 'multishot', 'fire rate / attack speed'],
    ['base damage / melee damage', 'multishot', 'status chance'],
    ['critical damage', 'multishot', 'status chance'],
    ['critical damage','multishot','punch_through']
]
#melee rolls
melee_filters = [
    ['critical damage', 'fire rate / attack speed', 'range'],
    ['base damage / melee damage', 'critical damage', 'critical chance'],
    ['critical chance', 'critical damage', 'channeling damage'],
    ['critical damage', 'fire rate / attack speed', 'channeling efficiency'],
    ['critical damage', 'fire rate / attack speed', 'heat damage'],
    ['critical damage','slash damage','base damage / melee damage'],
]
#meme rolls
meme_rolls = [
    ['impact damage','slash damage','puncture damage'],
    ['damage to corpus','damage to grineer','damage to infested']
]