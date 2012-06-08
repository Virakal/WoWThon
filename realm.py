import wowthon

class Realm(wowthon._FetchMixin):
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
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + \
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
        
    @property
    def auctions(self):
        """
        Returns a `wowthon.AuctionListings` object for the realm's auction
        houses.
        
        Note: These can be very slow calls as they block on large data
        downloads.
        
        """
        return wowthon.AuctionListings(self._api, self.slug, self.region)
        
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
        return self._api.get_char(name, self.slug, self.region,
                        initial_fields)