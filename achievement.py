import wowthon

# TODO How to deal with criteria

class Achievement(wowthon._FetchMixin):
    """
    Encapsulate a WoW achievement.
    
    """
    
    _PATH = 'achievement/'
    
    def __init__(self, api, id, region=None, locale=None, json=None):
        """
        Create a new Achievement using the specified api corresponding to
        the achievement `id`.
        
        Arguments:
        api -- the WoWAPI instance to use
        id -- the ID of the desired achievement
        
        Optional arguments:
        region -- the API region to use (default: api default)
        locale -- the locale to use (default: api default)
        json -- a dictionary to use instead of fetching from the server
                (default: None)
        
        """
        if not region: region = api.region
        if not locale: locale = api.locale
        self._api = api
        self._id = id
        self._json = json
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + str(id)
        
    @property
    def id(self):
        """Return the id of the achievement."""
        return self._id
        
    @property
    def title(self):
        """Return the title, or name, of the achievement."""
        return self._json_property('title')
        
    @property
    def points(self):
        """Return the number of points the achievement is worth."""
        return self._json_property('points')
        
    @property
    def description(self):
        """Returns the achievement description."""
        return self._json_property('description')
        
    @property
    def reward(self):
        """
        Return a string defining the reward for the achievement.
        
        Returns None if there is no reward.
        
        """
        try:
            return self._json_property('reward')
        except KeyError:
            # Achievement doesn't have a reward
            return None
            
    @property
    def reward_items(self):
        """
        Returns a list of Item objects representing achievement rewards.
        
        Returns None if the achievement does not have a reward or an
        empty list for an achievement with rewards that rewards no
        items.
        
        """
        # TODO Pass json and test it
        try:
            rewards = self._json_property('rewardItems')
        except KeyError:
            # No rewards
            return None
        ret = []
        for reward in rewards:
            ret.append(wowthon.Item(self._api, reward['id']))
        return ret
        
    @property
    def icon(self):
        """
        Returns the name of the achievement's icon.
        
        Use `Achievement.icon_url` to generate a URL for the icon.
        
        """
        return self._json_property('icon')
        
    @property
    def criteria(self):
        """
        Returns a list of dictionaries representing achievement criteria.
        The dictionary contains the following fields:
        
        id -- a criteria id
        description -- a criteria description
        
        """
        return self._json_property('criteria')
        
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