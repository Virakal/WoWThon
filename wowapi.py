# Imports
import urllib.request
from urllib.error import HTTPError #, URLError # Need URLError?
import json as jsonlib

# Package Imports
import wowthon

class WoWAPI(wowthon._FetchMixin):
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
        if type(realm) == wowthon.Realm:
            realm = realm.slug
        realm = self.realm_name_to_slug(realm)
        
        self.region = region.lower()
        self.realm = realm
        self.private_key = private_key
        self.public_key = public_key
        self.region_prefix = wowthon.REGION[self.region]['prefix']
        if not locale:
            # Or use the default locale if none is set
            self.locale = ''
        elif self._locale_case(locale) in \
            wowthon.REGION[self.region]['locales']:
            # Ensure locale is valid for region
            self.locale = self._locale_case(locale)
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
        
    @staticmethod
    def stat_string(id, amount):
        """
        Takes a stat id and amount and produces an English string representing
        the way that it would appear in the tooltip.
        
        For example:
            stat_string(7,130) returns:
            '+130 stamina'
        
        """
        return wowthon.STAT_IDS[id].format(amount=amount)
    
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
        url = wowthon.REGION[region]['prefix'] + 'realm/status'
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
            locale = kwargs['locale']
        except KeyError:
            locale = self.locale
        
        ret = []
        for realm in realms:
            ret.append(wowthon.Realm(self, realm, region, locale))
        return ret
        
    def get_guild(self, name, realm=None, region=None, initial_fields=None):
        """
        Return a Guild object for the specified guild.
        
        """
        return wowthon.Guild(self, name, realm, region, initial_fields)
        
    def get_char(self, name, realm=None, region=None, initial_fields=[]):
        """
        Get a Character object for the specified character.
        
        """
        return wowthon.Character(self, name, realm, region, initial_fields)
        
    def get_achieve(self, id, region=None, locale=None):
        """
        Get an Achievement object for the specified ID.
        
        """
        return wowthon.Achievement(self, id, region=region, locale=locale)
        
    def get_quest(self, id, region=None, locale=None):
        """
        Return a Quest object for the specified ID.
        
        """
        return wowthon.Quest(self, id, region=region, locale=locale)
        
    def get_item(self, id, region=None, locale=None):
        """
        Return an Item object for the specified ID.
        
        """
        return wowthon.Item(self, id, region=region, locale=locale)