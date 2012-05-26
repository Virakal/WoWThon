__author__ = 'Jonathan Goodger (jonno.is@gmail.com) (Untamedbush@Draenor-EU)'
__version__ = '0.2.1a'

__all__ = [
    'WoWAPI', 'Realm', 'Guild', 'GuildEmblem', 'Character', 'Auction', 
    'AuctionListings', 'Item', 'TalentSpec', 'Quest', 'Achievement'
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
from wowthon.item import Item
from wowthon.quest import Quest
from wowthon.achievement import Achievement

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

#
# Global constants
#

#: A list of valid regions.
REGIONS = ['eu', 'us', 'kr', 'tw', 'cn']

# TODO Consider dropping 'api/wow/' from prefixes, make functions in
#      WoWAPI that returns these values and add it there
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

#: A list of valid arena team sizes
TEAM_SIZES = [
    '5v5',
    '3v3',
    '2v2'
]

#: A dictionary mapping faction level ids to their English names
FACTION_LEVELS = {
    0 : 'hated'
    1 : 'hostile',
    2 : 'unfriendly',
    3 : 'neutral',
    4 : 'friendly',
    5 : 'honored',
    6 : 'revered',
    7 : 'exalted',
}

#
# Exceptions
#

# TODO ...