# TODO Currently a dummy
# NOTE http://tw.media.blizzard.com/wow/icons/56/inv_helmet_plate_raidpaladin_i_01.jpg
import wowthon

class Item(wowthon._FetchMixin):
    """
    Encapsulates a WoW item.
    
    """
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
        
    @property
    def description(self):
        """
        Return the item's description, or flavour text.
        
        Returns an empty string if the item has no flavour text.
        
        """
        return self._json_property('description')
        
    @property
    def icon(self):
        """Returns the name of the icon for the item."""
        return self._json_property('icon')
        
    @property
    def stack_size(self):
        """
        Returns the number of items that can be stacked in a single
        inventory slot.
        
        """
        return self._json_property('stackable')
        
    @property
    def stackable(self):
        """
        Returns True if the item is stackable.
        
        """
        return False if self.stack_size == 1 else True

    @property
    def allowable_classes(self):
        """
        Returns a list of class IDs for the classes able to use the item.
        
        Returns None if the item is not class restricted.
        
        """
        try:
            return self._json_property('allowableClasses')
        except KeyError:
            return None
            
    @property
    def class_restricted(self):
        """
        Returns True if the item may only be equipped by certain
        classes.
        
        """
        return True if self.allowable_classes else False
        
    @property
    def allowable_races(self):
        """
        Returns a list of race IDs for the races able to use the item.
        
        Returns None if the item is not race restricted.
        
        """
        try:
            return self._json_property('allowableRaces')
        except KeyError:
            return None
            
    @property
    def race_restricted(self):
        """
        Returns True if the item may only be equipped by certain
        races.
        
        """
        return True if self.allowable_races else False
        
    @property
    def binds(self):
        """
        Returns an integer defining how the item binds.
        
        Possible return codes are as follows:
        0 -- item does not bind
        1 -- binds on pickup or to account
        2 -- binds on equip
        
        """
        return self._json_property('itemBind')
        
    @property
    def stats(self):
        """
        Return a list of disctionaries representing the item's bonus stats.
        
        Note that this does not include armor. The dictionary has the
        following fields:
        
        stat -- a stat id
        amount -- the amount of the given stat
        reforged -- true if that stat has been reforged
        
        """
        return self._json_property('bonusStats')
        
    def icon_url(self, size=56):
        """
        Returns a URL to the icon on the Blizzard servers of the specified
        size. Valid sizes can be found in `wowthon.ICON_SIZES`.
        
        Optional arguments:
        size -- the size of the icon (default: 56)
        
        """
        region = self._api.region
        url = 'http://' + region + '.media.blizzard.com/wow/icons/'+ \
               str(size) + '/' + self.icon + '.jpg'
        return url
        