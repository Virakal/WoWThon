"""
File: wowthon.py
Author: Jonathan Goodger (Untamedbush @ Draenor-EU)
Date: 2012-05-03
Version: 0.1.5

"""

# TODO Split in to separate files and package
# TODO Get exceptions in place
# TODO Come up with better class documentation (and description up top)
# TODO Find out what does and doesn't use locale
# TODO A lot of data structures probably need cloning for immutability
# TODO Eventually replace (most) dictionaries with WoWAPI methods
# TODO Cache objects that already exist (don't duplicate realms, chars etc.)
# TODO Consider using dict.get instead of try: except KeyError
# TODO Consider making region info dictionaries instead of lists
# TODO Characters under level 10, you say?

import urllib.request
from urllib.error import HTTPError #, URLError # Need URLError?
import json as jsonlib
import unicodedata

# Global constants
#: A list of valid regions.
REGIONS = ['eu', 'us', 'kr', 'tw', 'cn']

#: A map of regions to their appropriate URL prefixes
REGION_PREFIXES = {
    'eu' : 'http://eu.battle.net/api/wow/',
    'us' : 'http://us.battle.net/api/wow/',
    'kr' : 'http://kr.battle.net/api/wow/',
    'tw' : 'http://tw.battle.net/api/wow/',
    'cn' : 'http://www.battlenet.com.cn/api/wow/'
}

#: A map of regions to their supported locales
SUPPORTED_LOCALES = {
    'us' : ['en_US', 'es_MX'],
    'eu' : ['en_GB', 'es_ES', 'fr_FR', 'ru_RU', 'de_DE'],
    'kr' : ['ko_KR'],
    'tw' : ['zh_TW'],
    'cn' : ['zh_CN']
}

# TODO Use this instead?
# TODO Consider dropping 'api/wow/' from prefixes, make functions in
#      WoWAPI that returns these values and add it there
#: A map of regions with their Battle.net prefixes and valid regions
REGION_DICTS = {
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
    #10 : '', # monk?
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

class _FetchMixin:
    """
    Mixin class to define common behaviour for any object that fetches data.
    
    """
    def _fetch(self, force=False):
        """
        Fetch the data from the WoW server if it has not already been
        downloaded.
        
        Arguments:
        force -- if true, fetches data regardless of whether the data
                 already exists.
        
        """
        # TODO Use last modified to refresh
        if force or not self._json:
            self._json = self._api._get_json(self._url)
            # Try to update last modified if it exists
            try:
                self._last_modified = self._json['lastModified']
            except KeyError:
                pass
            
    def force_update(self):
        """Force the data to update itself from the server."""
        self._fetch(force=True)
        
    def _json_property(self, name):
        """
        Get the property from the JSON object with the name `name`.
        
        Fetches the data from the server if necessary. This method will update
        the object's requested fields if necessary to retrieve the data asked
        of it. After requesting optional data, this data will be fetched with
        every subsequent update.
        
        """
        try:
            # Check if object has a _fields property
            self._fields
            has_fields = True
        except AttributeError:
            has_fields = False
            
        self._fetch()
        try:
            return self._json[name]
        except KeyError:
            if has_fields and name in self._fields:
                # If we don't have it, but we should have it, we force update
                self.force_update()
                return self._json[name]
            else:
                # Otherwise, we don't know what it is
                raise
                
    def _add_field(self, name):
        """
        Add a field to the list of fields fetched.
        
        """
        if name not in self._fields:
            self._fields.append(name)
            self._url = self._generate_url()
    
class WoWAPI(_FetchMixin):
    """
    Encapsulates an API connection for a given realm.
    
    """
    # TODO Maybe move static methods out
    
    # A dictionary for translating realm names to slugs
    _SLUG_TRANSLATION_DICTIONARY = {
        ord(' ')  : '-',
        ord('(')  : '',
        ord(')')  : '',
        ord('\'') : '',
        ord('é')  : 'e',
        ord('ü')  : 'u',
        ord('ê')  : 'e'
    }
    
    # NOTE This is needed to make the function idempotent,
    #      which makes it far more useful
    _SLUG_TRANSLATION_SPECIAL_CASES = {
        'azjol-nerub' : 'azjolnerub',
        'arak-arahm'  : 'arakarahm'
    }
    
    def __init__(self, realm, region='us', locale='',
                 private_key='', public_key=''):
        """
        Construct a new WoWAPI for the specified realm.
        
        The region for the API is set using the `region` argument.
        
        
        Arguments:
        realm -- the WoW realm on which the API will operate
        
        Keyword Arguments:
        region -- the server region (default 'us')
        locale -- the locale to use (default '')
        private_key -- your private API key (default '')
        public_key -- your public API key (default '')
        
        Throws:
        ValueError -- if the locale is not valid for the region
        
        """
        # TODO Implement public and private key
        if type(realm) == Realm:
            realm = realm.slug
        realm = self.realm_name_to_slug(realm)
        
        self.region = region.lower()
        self.realm = realm
        self.private_key = private_key
        self.public_key = public_key
        self.region_prefix = REGION_PREFIXES[self.region]
        if self._locale_case(locale) in SUPPORTED_LOCALES[self.region]:
            # Ensure locale is valid for region
            self.locale = self._locale_case(locale)
        elif not locale:    
            # Or use the default locale if none is set
            self.locale = ''
        else:
            raise ValueError('Illegal locale "' + locale +
                            '" passed for region "' + self.region + '".')
        
    @staticmethod
    def _locale_case(s):
        """
        Convert the passed locale string to normal locale case.
        
        e.g.
        "en_gb" becomes:
            "en_GB"
            
        "EN_US" becomes:
            "en_US"
        
        """
        lang, dialect = tuple(s.split('_'))
        return lang.lower() + '_' + dialect.upper()
        
    @staticmethod
    def to_money_string(cash): 
        """
        Convert an integer to WoW money.

        e.g.
        128773 becomes:
            12g 87s 73c
            
        17 becomes:
            17c
            
        1200 becomes:
            12s 0c
            
        """
        # Record negativity
        neg = (cash < 0)
        i = abs(cash)
        # copper
        ret = str(i % 100) + 'c'
        # silver
        i = i // 100
        if i > 0:
            ret = str(i % 100) + 's ' + ret
        # gold
        i = i // 100
        if i > 0:
            ret = str(i) + 'g ' + ret
            
        # Prepend '-' if negative
        if neg: ret = '-' + ret
        return ret.strip()
    
    @staticmethod
    def strip_zero_denominations(money_string):
        """
        Removes smaller denominations from a money string when they are zero.

        e.g.
        "6000g 0s 0c" becomes:
            "6000g"

        "6000g 10s 0c" becomes:
            "6000g 10s"

        "6000g 0s 12c" is not changed.
        
        """
        if len(money_string) > 3:
            if money_string[-3:] == ' 0c':
                money_string = money_string[:-3]
            if money_string[-3:] == ' 0s':
                money_string = money_string[:-3]
        return money_string
    
    @staticmethod
    def realm_name_to_slug(name):
        """
        Transform a realm name in to a slug name.
        
        e.g.
        "Draenor" becomes:
            "dreanor"
            
        "Aggra (Português)" becomes:
            "aggra-portugues"
        
        Note: `test_all_realm_to_slug_names.py` tests this for all realms
              in all regions.
        
        """
        # All slugs are lowercase
        ret = name.lower()
        
        # Slug rules strip dashes, but I don't want to automatically
        if ret in WoWAPI._SLUG_TRANSLATION_SPECIAL_CASES:
            return WoWAPI._SLUG_TRANSLATION_SPECIAL_CASES[ret]
        
        ret = ret.translate(WoWAPI._SLUG_TRANSLATION_DICTIONARY)
        return ret
       
    @staticmethod   
    def side_for_race(id):
        """
        Return the side id for a given race id.
        
        """
        # TODO Consider using data API for this
        ally = [11,1,7,3,4,22]
        horde = [5,8,2,10,6,9]
        
        if id in ally: return 0
        if id in horde: return 1
    
    def _get_json(self, url):
        """Make a dictionary from the JSON file at `url`"""
        # TODO Error checking, from urllib and external
        # TODO Implement API keys here
        req = urllib.request.urlopen(url)
        return jsonlib.loads(str(req.read(), 'UTF-8'))
        
    def _get_locale_suffix(self, prefix='?', locale=None):
        """
        Return a URL suffix for the specified locale.
        If no locale is specified, the current API's locale is used.
        
        Arguments:
        prefix -- The characters to use before the locale string (default '?')
        locale -- The locale to use (default None)
        
        """
        #if not self.locale: return prefix # FIXME What was I doing here?
        if not locale and not self.locale:
            locale = ''
        elif not locale:
            locale = self.locale
        return prefix + 'locale=' + locale
    
    def list_all_realm_names(self, region=None):
        """
        List the slug of every realm in the specified region.
        
        If no region is specified, the current API's region is used.
        
        """
        if not region: region = self.region
        url = REGION_PREFIXES[region] + 'realm/status'
        json = self._get_json(url)
        ret = []
        for realm in json['realms']:
            ret.append(realm['slug'])
        return ret
        
    def get_realm(self, *realms, **kwargs):
        """
        Get a realm object.
        
        Returns a list of Realm objects, in order of specification.
        
        If no realm or region are specified the API's current settings
        are used.
        
        Arguments:
        realms -- A list of realms to check (default current realm)
        
        Keyword Arguments:
        region -- The API region to use (default current region)
        locale -- The locale to return (default current locale)
        
        """
        # TODO Is a list really useful?
        # TODO Does locale matter?
        
        if not realms: realms = [self.realm]
        try:
            region = kwargs['region']
        except KeyError:
            region = self.region
        
        try:
            region = kwargs['locale']
        except KeyError:
            locale = self.locale
        
        ret = []
        for realm in realms:
            ret.append(Realm(self, realm, region, locale))
        return ret
        
    def get_guild(self, name, realm=None, region=None, initial_fields=None):
        """
        Return a Guild object for the specified guild.
        
        """
        return Guild(self, name, realm, region, initial_fields)
        
    def get_char(self, name, realm, region=None, initial_fields=[]):
        """
        Get a Character object for the specified character.
        
        """
        return Character(self, name, realm, region, initial_fields)
        
class Realm(_FetchMixin):
    """
    Encapsulates a realm.
    
    """
    
    #: The path to the correct part of the API
    _PATH = 'realm/status?realms='
    
    def __init__(self, api, name=None, region=None, locale=None):
        """
        Build a new Realm object for the specified realm.
        
        If the optional arguments are not specified, the passed API's
        settings are used.
        
        Arguments:
        api -- an instance of WoWthon to use
        
        Optional Orguments:
        name -- the name of the realm to fetch
        region -- the API region to fetch the realm from
        locale -- the locale to use for data
        
        """
        # TODO Auction data :)
        if not region: region = api.region
        if not locale: locale = api.locale
        if not name: name = api.realm
        name = api.realm_name_to_slug(name)
        
        self._region = region
        self._locale = locale
        self._json = None
        self._api = api
        self._url = REGION_PREFIXES[region] + self._PATH + \
                    name + api._get_locale_suffix('&')
    
    def _fetch(self, force=False):
        super()._fetch()
        try:
            # Only returns one realm.
            self._json = self._json['realms'][0]
        except KeyError:
            # Already been done, presumably.
            pass
        
    @property
    def name(self):
        """The name of the realm."""
        return self._json_property('name')
        
    @property
    def slug(self):
        """The slug for referring to the realm internally."""
        return self._json_property('slug')
    
    @property
    def battlegroup(self):
        """The realm's battlegroup."""
        return self._json_property('battlegroup')
    
    @property
    def is_online(self):
        """Returns true if the realm is online."""
        return self._json_property('status')
    
    @property
    def queue(self):
        """Returns true if the realm has a login queue."""
        return self._json_property('queue')
        
    @property
    def type(self):
        """Returns the realm type."""
        return self._json_property('type')
        
    @property
    def population(self):
        """Returns the population level of the realm."""
        return self._json_property('population')
        
    @property
    def region(self):
        """Returns the region of the specified realm."""
        # NOTE Does not need a fetch
        return self._region
        
    def pvp_zone_status(self, zone):
        """
        Return a dictionary representing the status of the specified PvP zone.
        
        Note: There is no caching for this function.
        
        """
        # TODO Consider a zone status object
        self.force_update()
        return self._json_property(zone)
        
    def list_pvp_zones(self):
        """
        Returns a list of PvP zone names.
        
        e.g. for Cataclysm this returns:
            ['wintergrasp', 'tol-barad']
            
        Note: The order is not guaranteed.
            
        """
        self._fetch()
        # NOTE Assumes all dicts returned are PvP zones
        # TODO Alphabetical sort?
        return [k for k in self._json.keys() if type(self._json[k]) == dict]
        
    def get_char(self, name, initial_fields=None):
        """
        Return the specified character from this realm.
        
        """
        return Character(self._api, name, self.slug, self.region, initial_fields)
        
class Guild(_FetchMixin):
    """
    Encapsulates a guild.
    
    """
    
    #: A list of possible fields to be passed to the API
    VALID_FIELDS = [
        'members',
        'achievements',
        'news'
    ]
    
    #: The path to the correct part of the API
    _PATH = 'guild/'
    
    def __init__(self, api, name, realm=None, region=None,
                 initial_fields=None, locale=None, json=None):
        """
        Creates a new Guild.
        
        `initial_fields` is a list of fields to fetch early. If you know you
        will be using Guild.members soon, for example, you may wish to set
        this to ['members'] to avoid making two API requests in succession.
        
        `initial_fields` should also be set to whatever is present in the data
        passed through the `json` parameter to avoid fetching data that is
        already present.
        
        Arguments:
        api -- the WoWAPI instance to use
        name -- the name of the guild to fetch
        
        Optional Arguments:
        realm -- the realm the guild resides on (default to api settings)
        region -- the region of the realm (default to api settings)
        initial_fields -- fields to request early
        locale -- the locale to use for the returned data
        json -- set this to construct the guild from previously fetched json
        
        """
        # TODO self.guild_rank(Character/Name)
        if not realm: realm = api.realm
        if not region: region = api.region
        if not initial_fields: initial_fields = []
        if type(realm) == Realm:
            realm = realm.slug
        realm = api.realm_name_to_slug(realm)
        
        self._fields = initial_fields
        self._region = region
        self._realm = realm
        self._name = name
        self._api = api
        
        self._url = self._generate_url()
        self._last_modified = None
        self._json = json
        
    def _generate_url(self, with_fields=True):
        """
        Generate the URL to use to fetch data from the API.
        
        If with_fields is true, the ?fields parameter will be populated.
        
        """
        # TODO Ensure fields are valid
        fields = ''
        if self._fields and with_fields:
            fields = '?fields='
            for field in self._fields:
                fields += field + ','
            assert fields[-1] == ','
            fields = fields[:-1] # chop off trailing comma
            
        return REGION_PREFIXES[self._region] + self._PATH + self._realm + \
               '/' + self._name + fields
        
    @property
    def level(self):
        """Return the guild level."""
        return self._json_property('level')
    
    @property
    def achievement_points(self):
        """Return the guild's achievement points."""
        return self._json_property('achievementPoints')
        
    @property
    def side(self):
        """
        Return the side id for the guild. This corresponds to the faction
        the guild is affiliated with.
        
        `wowthon.SIDES` maps these IDs to their English equivalents.
        
        """
        return self._json_property('side')
        
    @property
    def realm(self):
        """Returns a Realm object detailing the realm the guild is on."""
        return self._json_property('realm')
        
    @property
    def battlegroup(self):
        """Returns the name of the battlegroup the realm is on."""
        return self._json_property('battlegroup')
        
    @property
    def name(self):
        """Returns the name of the guild."""
        return self._json_property('name')
        
    @property
    def region(self):
        """Returns the region code (two letters) for the realm the guild is on."""
        return self._region
        
    @property
    def emblem(self):
        """Returns a GuildEmblem object detailing the guild's chosen emblem."""
        return GuildEmblem(self._json_property('emblem'))
        
    @property
    def members(self):
        """
        Return a list of tuples of the form:
            (rank, char)
            
        where `rank` is an integer representing the character's guild rank
        and `char` is a Character object representing the character.
        
        """
        # TODO Consider dropping tuple
        self._add_field('members')
        member_list = self._json_property('members')
        ret = []
        for member in member_list:
            char = Character(
                              self._api,
                              member['character']['name'],
                              self.realm,
                              self.region,
                              json=member['character']
                             )
            char._g_rank = member['rank']
            ret.append((member['rank'],char))
                                  
        return ret
        
    @property
    def news(self):
        """
        Returns a list of dictionaries representing guild news items.
        
        The structure of these dictionaries is defined in the CP API
        documentation.
        
        """
        # TODO Make objects?
        # TODO Test me
        self._add_field('news')
        if 'news' not in self._fields:
            # TODO Smarter way to do this?
            self._fields.append('news')
            self._url = self._generate_url()
            
        return self._json_property('news')
        
    @property
    def achievements(self):
        self._add_field('achievements')    
        return self._json_property('achievements')
        
class GuildEmblem:
    """
    Encapsulates a guild's emblem.
    
    """
    # TODO Draw itself?
    def __init__(self, json):
        """
        Builds a new emblem from the supplied dictionary.
        
        """
        self._json = json
        
    @property
    def icon(self):
        """The id number of the icon chosen for the guild emblem."""
        return self._json['icon']
    
    @property
    def icon_color(self):
        """The color of the emblem in ARGB format."""
        return self._json['iconColor']
        
    @property
    def border(self):
        """The id number for the border type."""
        return self._json['border']
        
    @property
    def border_color(self):
        """The color of the border in ARGB format."""
        return self._json['borderColor']
        
    @property
    def bg_color(self):
        """The background color in ARGB format."""
        return self._json['backgroundColor']
        
class Character(_FetchMixin):
    """
    Encapsulates an in-game character.
    
    """
    # TODO Finish implementation
    # TODO Document properties
    
    #: A list of possible fields to be passed to the API
    VALID_FIELDS = [
        'guild',
        'stats',
        'feed',
        'talents',
        'items',
        'reputation',
        'titles',
        'professions',
        'appearance',
        'companions',
        'mounts',
        'pets',
        'acheivements',
        'progression',
        'pvp',
        'quests'
    ]
    
    _PATH = 'character/'
    
    def __init__(self, api, name, realm=None, region=None, initial_fields=None,
                 json=None):
        # TODO Document
        if not realm: realm = api.realm
        if not region: region = api.region
        if not initial_fields: initial_fields = []
        if type(realm) == Realm:
            realm = realm.slug
        realm = api.realm_name_to_slug(realm)
        
        self._api = api
        self._name = name
        self._realm = realm
        self._region = region
        self._fields = initial_fields
        self._json = json
        self._url = self._generate_url()
        self._g_rank = None
        self._current_title = None
        
    def _generate_url(self, with_fields=True):
        """
        Generate the URL to use to fetch data from the API.
        
        If with_fields is true, the ?fields parameter will be populated.
        
        """
        # TODO Ensure fields are valid
        fields = ''
        if self._fields and with_fields:
            fields = '?fields='
            for field in self._fields:
                fields += field + ','
            assert fields[-1] == ','
            fields = fields[:-1] # chop off trailing comma
        return REGION_PREFIXES[self._region] + self._PATH + self._realm + \
               '/' + self._name + fields
               
    def title_string(self, id):
        """
        Returns the title for a given id with the player's name
        substituted in.
        
        e.g. (For a player named 'Jon')
        title_string(164) returns:
            "Starcaller Jon"
            
        title_string(175) returns:
            "Jon the Kingslayer"
        
        """
        title = next(filter((lambda t: t['id'] == id), self.titles))['name']
        return title.replace('%s', self.name)
    
    @property
    def name(self):
        """Returns the name of the character."""
        return self._json_property('name')
        
    @property
    def race(self):
        """
        Returns the race ID for the character.
        
        `wowthon.RACES` maps these IDs to their English equivalents.
        
        """
        return self._json_property('race')
        
    @property
    def region(self):
        """Returns the region code the character is from."""
        return self._region
        
    @property
    def battlegroup(self):
        """Returns the name of the battlegroup the character's realm is on."""
        return self._json_property('battlegroup')
        
    @property
    def gender(self):
        """
        Returns the gender ID of the player.
        
        `wowthon.GENDERS` provides a map of these to their
        English equivalents.
        
        """
        return self._json_property('gender')
        
    @property
    def class_(self):
        """
        Returns the class ID of the player.
        
        `wowthon.CLASSES` provides a map of these to their
        English equivalents.
        
        """
        return self._json_property('class')
        
    @property
    def level(self):
        """Returns the level of the player."""
        return self._json_property('level')
        
    @property
    def achievement_points(self):
        """
        Returns the number of achievement points the player has obtained.
        
        The data for the achievements can be obtained using
        Character.achievements. [NYI]
        """
        return self._json_property('achievementPoints')
        
    @property
    def side(self):
        """
        Return the side id for the player. This corresponds to the faction
        that the player plays for.
        
        `wowthon.SIDES` provides a map of these to their English equivalents.
        
        """
        return WoWAPI.side_for_race(self._json_property('race'))
        
    @property
    def thumbnail_url(self):
        """Returns a URL to a thumbnail image of the character."""
        # TODO add regional prefix
        return self._json_property('thumbnail')
        
    @property
    def guild_rank(self):
        """
        Returns an integer representing the guild rank of the character.
        
        Returns None if the player is not in a guild.
        
        """
        # TODO Get rank if not already fetched
        return self._g_rank
        
    @property
    def realm(self):
        """
        Returns a Realm object representing the realm the
        character is on.
        
        """
        realmname = self._json_property('realm')
        return Realm(self._api, 
                     WoWAPI.realm_name_to_slug(realmname),
                     self.region
                    )
    @property   
    def titles(self):
        """
        Returns a list of dictionaries representing titles the player
        has earned. Returns an empty list if no titles have yet been earned.
        
        A title dictionary is in the following form:
            {
                'id' : int,
                'name' : str,
                'selected' : bool
            }
        
        where `id` is the id of the title, `name` is a string representing
        the title itself, with '%s' in place of the character name
        (e.g. "%s, Destroyer's End") and `selected` is True if the title
        is the title currently chosen for the character.
        
        A title can be "pretty printed" using
        Character.title_string(char, id).
        
        """
        # TODO Return None if no titles
        # NOTE This loops through every time it's called
        self._add_field('titles')
        titles = self._json_property('titles')
        for title in titles:
            try:
                if title['selected']:
                    self._current_title = title
            except KeyError:
                # Not selected, add false
                title['selected'] = False
        return titles
        
    @property
    def current_title(self):
        """
        Returns a title dictionary for the title currently chosen by the
        character. The structure of the dictionary is defined in
        `Character.titles`'s help.
        
        Returns None if no title has been chosen by the character.
        
        """
        if not self._current_title:
            if 'titles' in self._fields:
                # If we've fetched titles already and it's still None
                # no title is selected.
                return None
            else:
                # Otherwise, we haven't fetched it yet!
                self.titles # Grab title data
        return self._current_title
        
    @property
    def guild(self):
        """
        Returns a Guild object representing the character's guild.
        
        Returns None if the character is unguilded.
        """
        # TODO Set guild rank (and make property)
        # TODO Return None for unguilded players.
        self._add_field('guild')
        guild = self._json_property('guild')
        return Guild(
                self._api,
                guild['name'],
                self.realm.slug,
                self.region,
                initial_fields=None,
                json=guild
               )
               
class Auction:
    """
    Encapsulates an individual auction.
    
    """
    def __init__(self, api, json, realm=None, region=None):
        """
        Creates an auction object from the supplied dictionary
        on the specified realm.
        
        Uses the API's default realm and region if none are specified.
        
        """
        # TODO Test
        # TODO Implement item
        if not realm:
            realm = api.realm
        if not region:
            region = api.region
            
        self._api = api
        self._json = json
        self._realm = realm
        self._region = region
        self._item = None
        self._owner = None
    
    @property
    def id(self):
        """Returns the auction id."""
        return self._json['auc']
        
    @property
    def owner(self):
        """
        Returns a Character object representing the owner of the
        auction.
        
        """
        if not self._owner:
            self._owner = Character(
                self._api,
                self._json['owner'],
                self._realm,
                self._region
            )
        return self._owner
        
    @property
    def bid(self):
        """Returns the current bid price on the item."""
        return self._json['bid']
        
    @property
    def buyout(self):
        """
        Returns the buyout price for the item.
        
        Returns X if there is no buyout specified.
        
        """
        # TODO Find out what is returned if there isn't a buyout
        return self._json['buyout']
        
    @property
    def quantity(self):
        """Returns the quanitity of items for sale."""
        return self._json['quantity']
        
    @property
    def item(self):
        """
        Returns an Item object representing the item up for auction.
        
        """
        # TODO Use Item object instead
        if not self_item:
            self._item = Item(
                               self._api,
                               self._json['item']
                              )
        return self._item
        
    @property
    def time_left(self):
        """
        Returns a string representing the approximate time left on an auction.
        
        """
        return self._json['timeLeft']
        
class Item:
    def __init__(self, api, id):
        self._api = api
        self._id
        
class AuctionListings(_FetchMixin):
    # TODO Do updates and last modified
    #: A list of valid auction house names
    AUCTION_HOUSES = [
        'alliance',
        'horde',
        'neutral'
    ]
    
    #: A list of possible values for time_left
    TIME_LEFT = [
        'VERY_LONG',
        'LONG',
        'SHORT'
    ]
    
    _PATH = 'auction/data/'
    
    def __init__(self, api, realm=None, region=None):
        if not realm:
            realm = api.realm
        if not region:
            region = api.region
        
        self._api = api
        self._realm = realm
        self._region = region
        self._json = None
        self._ah_json = None
        self._url = REGION_PREFIXES[self._region] + self._PATH + self._realm
        self._auctions = {}
        self._last_modified = 0
        
    def _get_data(self):
        if not self._ah_json:
            # TODO Check last modified
            # Get the file URL
            url = self._json_property('files')[0]['url']
            # Download the data
            fp = urllib.request.urlopen(url)
            # Read and convert to UTF-8 (json doesn't work on bytes)
            data = fp.readall().decode('utf-8')
            # Interpret the JSON
            self._ah_json = jsonlib.loads(data)
            

    def auctions(self, ah):
        """
        Returns a list of auctions from the sepcified auction house.
        
        Valid auction houses are listed in `AuctionListings.AUCTION_HOUSES`
        
        """
        self._get_data()
        data = self._auctions.get(ah)
        if not data:
            # Auction objects have not yet been built
            auctions = self._ah_json[ah]['auctions']
            data = []
            for auction in auctions:
                data.append(Auction(self._api, auction))
            self._auctions[ah] = data
        return data
        
    def all_auctions(self):
        ret = []
        for ah in AuctionListings.AUCTION_HOUSES:
            ret.extend(self.auctions(ah))
        return ret