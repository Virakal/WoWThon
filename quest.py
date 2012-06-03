import wowthon

class Quest(wowthon._FetchMixin):
    """
    Encapsulates a WoW quest.
    
    """
    _PATH = 'quest/'
    def __init__(self, api, id, region=None, locale=None, json=None):
        """
        Create a new Quest object using the specified API, for the quest `id`.
        
        Arguments:
        api -- the WoWAPI instance to use
        id -- the ID of the desired quest
        
        Optional arguments:
        region -- the API region to use (default: api default)
        locale -- the locale to use (default: api default)
        json -- a dictionary to use instead of fetching from the server
                (default: None)
        
        """
        # TODO Implement locale
        if not region: region = api.region
        if not locale: locale = api.locale
        self._api = api
        self._id = id
        self._json = json
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + str(id)
        
    @property
    def id(self):
        """Return the quest id."""
        return self._id
        
    @property
    def title(self):
        """Return the title, or name, of the quest."""
        return self._json_property('title')
        
    @property
    def req_level(self):
        """Return the minimum required level for the quest."""
        return self._json_property('reqLevel')
        
    @property
    def suggested_party_members(self):
        """Return the number of suggested party members for the quest."""
        return self._json_property('suggestedPartyMembers')
        
    @property
    def category(self):
        """Return the quest category associated with the quest."""
        return self._json_property('category')
        
    @property
    def level(self):
        """Return the level of the quest."""
        return self._json_property('level')
