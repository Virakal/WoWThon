__author__ = 'Jonathan Goodger (jonno.is@gmail.com) (Untamedbush@Draenor-EU)'
__version__ = '0.3.0a'

__all__ = [
    'WoWAPI', 'Realm', 'Guild', 'GuildEmblem', 'Character', 'Auction',
    'AuctionListings', 'Item', 'TalentSpec', 'Quest', 'Achievement',
    'ItemSet', 'ArenaTeam', 'APIError'
]

#
# Package imports
#
from wowthon.fetch import _FetchMixin
from wowthon.wowapi import WoWAPI
from wowthon.realm import Realm
from wowthon.guild import Guild, GuildEmblem
from wowthon.character import Character, TalentSpec
from wowthon.auctions import Auction, AuctionListings
from wowthon.item import Item, ItemSet
from wowthon.quest import Quest
from wowthon.achievement import Achievement
from wowthon.pvp import ArenaTeam
from wowthon.exceptions import APIError

# Hide package structure
del fetch
del wowapi
del realm
del guild
del character
del auctions
del item
del quest
del achievement
del pvp
del exceptions

#
# Global constants
#

#: A list of valid regions.
REGIONS = ['eu', 'us', 'kr', 'tw', 'cn']

#: A map of regions with their Battle.net prefixes and valid regions
REGION = {
    'eu' : {
        'prefix'  : 'http://eu.battle.net/api/wow/',
        'locales' : ['en_GB', 'es_ES', 'fr_FR', 'ru_RU', 'de_DE']
    },
    'us' : {
        'prefix'  : 'http://us.battle.net/api/wow/',
        'locales' : ['en_US', 'es_MX']
    },
    'kr' : {
        'prefix'  : 'http://kr.battle.net/api/wow/',
        'locales' : ['ko_KR']
    },
    'tw' : {
        'prefix'  : 'http://tw.battle.net/api/wow/',
        'locales' : ['zh_TW']
    },
    'cn' : {
        'prefix'  : 'http://www.battlenet.com.cn/api/wow/',
        'locales' : ['zh_CN']
    }
}

# TODO Possibly make these dicts, with HTML colors and stuff
#: A map of item quality numbers to their English descriptions
ITEM_QUALITY = {
    0 : 'poor',
    1 : 'common',
    2 : 'uncommon',
    3 : 'rare',
    4 : 'epic',
    5 : 'legendary',
    6 : 'artifact',
    7 : 'heirloom'
}

#: A map of race IDs to their English names.
RACES = {
    1  : 'human',
    2  : 'orc',
    3  : 'dwarf',
    4  : 'night elf',
    5  : 'undead',
    6  : 'tauren',
    7  : 'gnome',
    8  : 'troll',
    9  : 'goblin',
    10 : 'blood elf',
    11 : 'draenei',
    22 : 'worgen'
}

#: A map of class IDs to their English names.
CLASSES = {
    1  : 'warrior',
    2  : 'paladin',
    3  : 'hunter',
    4  : 'rogue',
    5  : 'priest',
    6  : 'death knight',
    7  : 'shaman',
    8  : 'mage',
    9  : 'warlock',
    11 : 'druid'
}

#: A map of genders to their English names.
GENDERS = {
    0 : 'male',
    1 : 'female'
}

#: A map of side IDs to their English faction names.
SIDES = {
    0 : 'alliance',
    1 : 'horde',
}

#: A list of valid icon sizes for Item.icon_url().
ICON_SIZES = [18, 36, 56]

#: A map of PvP zone statuses to their English descriptions
PVP_ZONE_STATUSES = {
    -1 : 'unknown',
    0  : 'idle',
    1  : 'populating',
    2  : 'active',
    3  : 'concluded'
}

#: A list of possible realm population levels
POPULATION_LEVELS = [
    'high',
    'medium',
    'low'
]

#: A list of possible realm types
REALM_TYPES = [
    'pvp',
    'pve',
    'rp',
    'rppvp',
]

#: A map of valid arena team sizes and their string equivalents
TEAM_SIZES = {
    2 : '2v2',
    3 : '3v3',
    5 : '5v5'
}

#: A dictionary mapping faction level ids to their English names
FACTION_LEVELS = {
    0 : 'hated',
    1 : 'hostile',
    2 : 'unfriendly',
    3 : 'neutral',
    4 : 'friendly',
    5 : 'honored',
    6 : 'revered',
    7 : 'exalted'
}

# Thanks to Ulminia for this
#: A map of stat ids to their English tooltip valuess
STAT_NAMES = {
    1  : '+{amount} Health',
    2  : '+{amount} Mana',
    3  : '+{amount} Agility',
    4  : '+{amount} Strength',
    5  : '+{amount} Intellect',
    6  : '+{amount} Spirit',
    7  : '+{amount} Stamina',
    46 : 'Equip: Restores {amount} health per 5 sec.',
    44 : 'Equip: Increases your armor penetration rating by {amount}.',
    38 : 'Equip: Increases attack power by {amount}.',
    15 : 'Equip: Increases your shield block rating by {amount}.',
    48 : 'Equip: Increases the block value of your shield by {amount}.',
    19 : 'Equip: Improves melee critical strike rating by {amount}.',
    20 : 'Equip: Improves ranged critical strike rating by {amount}.',
    32 : 'Equip: Increases your critical strike rating by {amount}.',
    21 : 'Equip: Improves spell critical strike rating by {amount}.',
    25 : 'Equip: Improves melee critical avoidance rating by {amount}.',
    26 : 'Equip: Improves ranged critical avoidance rating by {amount}.',
    34 : 'Equip: Improves critical avoidance rating by {amount}.',
    27 : 'Equip: Improves spell critical avoidance rating by {amount}.',
    12 : 'Equip: Increases defense rating by {amount}.',
    13 : 'Equip: Increases your dodge rating by {amount}.',
    37 : 'Equip: Increases your expertise rating by {amount}.',
    40 : 'Equip: Increases attack power by {amount} in Cat, Bear, ' + \
         'Dire Bear, and Moonkin forms only.',
    28 : 'Equip: Improves melee haste rating by {amount}.',
    29 : 'Equip: Improves ranged haste rating by {amount}.',
    36 : 'Equip: Increases your haste rating by {amount}.',
    30 : 'Equip: Improves spell haste rating by {amount}.',
    16 : 'Equip: Improves melee hit rating by {amount}.',
    17 : 'Equip: Improves ranged hit rating by {amount}.',
    31 : 'Equip: Increases your hit rating by {amount}.',
    18 : 'Equip: Improves spell hit rating by {amount}.',
    22 : 'Equip: Improves melee hit avoidance rating by {amount}.',
    23 : 'Equip: Improves ranged hit avoidance rating by {amount}.',
    33 : 'Equip: Improves hit avoidance rating by {amount}.',
    24 : 'Equip: Improves spell hit avoidance rating by {amount}.',
    43 : 'Equip: Restores {amount} mana per 5 sec.',
    49 : 'Equip: Increases your mastery rating by {amount}.',
    14 : 'Equip: Increases your parry rating by {amount}.',
    39 : 'Equip: Increases ranged attack power by {amount}.',
    35 : 'Equip: Increases your resilience rating by {amount}.',
    41 : 'Equip: Increases damage done by magical spells and effects ' + \
         'by up to {amount}.',
    42 : 'Equip: Increases healing done by magical spells and effects ' + \
         'by up to {amount}.',
    47 : 'Equip: Increases spell penetration by {amount}.',
    45 : 'Equip: Increases spell power by {amount}.'
}

# Thanks to Zonous
#: A map of reforge ids to a tuple. The first element of the tuple is the
#: id of the stat to reforge from, the second is the id of the stat to
#: reforge to.
REFORGES = {
    113 : (6, 13),
    114 : (6, 14),
    115 : (6, 31),
    116 : (6, 32),
    117 : (6, 36),
    118 : (6, 37),
    119 : (6, 49),
    120 : (13, 6),
    121 : (13, 14),
    122 : (13, 31),
    123 : (13, 32),
    124 : (13, 36),
    125 : (13, 37),
    126 : (13, 49),
    127 : (14, 6),
    128 : (14, 13),
    129 : (14, 31),
    130 : (14, 32),
    131 : (14, 36),
    132 : (14, 37),
    133 : (14, 49),
    134 : (31, 6),
    135 : (31, 13),
    136 : (31, 14),
    137 : (31, 32),
    138 : (31, 36),
    139 : (31, 37),
    140 : (31, 49),
    141 : (32, 6),
    142 : (32, 13),
    143 : (32, 14),
    144 : (32, 31),
    145 : (32, 36),
    146 : (32, 37),
    147 : (32, 49),
    148 : (36, 6),
    149 : (36, 13),
    150 : (36, 14),
    151 : (36, 31),
    152 : (36, 32),
    153 : (36, 37),
    154 : (36, 49),
    155 : (37, 6),
    156 : (37, 13),
    157 : (37, 14),
    158 : (37, 31),
    159 : (37, 32),
    160 : (37, 36),
    161 : (37, 49),
    162 : (49, 6),
    163 : (49, 13),
    164 : (49, 14),
    165 : (49, 31),
    166 : (49, 32),
    167 : (49, 36),
    168 : (49, 37)
}
