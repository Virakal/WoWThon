# TODO Currently a dummy
# NOTE http://tw.media.blizzard.com/wow/icons/56/inv_helmet_plate_raidpaladin_i_01.jpg
import wowthon

class Item(wowthon._FetchMixin):
    _PATH = 'item/'
    def __init__(self, api, id, region=None, locale=None, json=None):
        """
        Create a new Item object using the specified API, for the Item `id`.
        
        Arguments:
        api -- the WoWAPI instance to use
        id -- the ID of the desired item
        
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
        """Return the id of the item."""
        return self._id
        
    @property
    def name(self):
        """Return the name of the item."""
        return self._json_property('name')