import wowthon

class Character(wowthon._FetchMixin):
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
        if type(realm) == wowthon.Realm:
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
        return wowthon.REGION[self._region]['prefix'] + self._PATH + \
               self._realm + '/' + self._name + fields
               
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
        return wowthon.WoWAPI.side_for_race(self._json_property('race'))
        
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
        return wowthon.Realm(self._api, 
                             wowthon.WoWAPI.realm_name_to_slug(realmname),
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
        return wowthon.Guild(
                             self._api,
                             guild['name'],
                             self.realm.slug,
                             self.region,
                             initial_fields=None,
                             json=guild
                            )
                            
    @property
    def stats(self):
        """
        Return a dictionary of the character's stats.
        
        """
        # TODO Stats object might be overkill, but could have useful stuff
        self._add_field('stats')
        return self._json_property('stats')
        
    @property
    def talents(self):
        # NOTE Tuple might not be good if triple spec is ever on the cards
        """
        Returns a tuple of `TalentSpec` objects.
        
        """
        self._add_field('talents')
        data = self._json_property('talents')
        if len(data) == 1:
            return (TalentSpec(data[0]),)
        else:
            return (TalentSpec(data[0]), TalentSpec(data[1]))
            
class TalentSpec:
    def __init__(self, data):
        self.name = data['name']