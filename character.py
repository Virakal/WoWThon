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
        
        Note: This is class_ as class is a keyword.
        
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
        # NOTE Order first and second or selected, unselected?
        """
        Returns a tuple of `TalentSpec` objects.
        
        """
        self._add_field('talents')
        data = self._json_property('talents')
        if len(data) == 1:
            return (TalentSpec(self._api, data[0]),)
        else:
            return (TalentSpec(self._api, data[0]), \
                    TalentSpec(self._api, data[1]))
                    
    @property
    def honor_kills(self):
        """Return the number of honorable kills a player has earned."""
        self._add_field('pvp')
        return self._json_property('pvp')['totalHonorableKills']
        
    @property
    def arena_teams(self):
        """
        Return a list of dictionaries representing the player's arena teams.
        The dictionary has the following fields:
        
        name -- the name of the team
        personal_rating -- the characters's personal rating
        team_rating -- the team's rating
        size -- the team size (c.f. wowthon.TEAM_SIZES)
        
        """
        self._add_field('pvp')
        teams = self._json_property('pvp')['arenaTeams']
        
        pyteams = []
        # Get rid of camel case
        for team in teams:
            pyteam = {
                'name' : team['name'],
                'personal_rating' : team['personalRating'],
                'team_rating' : team['teamRating'],
                'size' : team['size']
            }
            pyteams.append(pyteam)
            
        return pyteams
        
    @property
    def rbg_rating(self):
        """Returns the character's personal rated battleground rating"""
        self._add_field('pvp')
        return self._json_property('pvp')['ratedBattlegrounds'] \
               ['personalRating']
        
    @property
    def rbg_info(self):
        """
        Returns a list of dictionaries detailing win data for each
        battleground. The dictionaries have the following fields:
        
        name -- the name of the battleground
        played -- the number of games played
        won -- the number of games won
        
        """
        # TODO Add win ratios? Totals?
        self._add_field('pvp')
        return self._json_property('pvp')['ratedBattlegrounds'] \
               ['battlegrounds']
        
class TalentSpec:
    """
    Encapsulated a talent specification.
    
    This mostly just exposes the dictionary currently.
    
    """
    def __init__(self, api, data):
        """
        Create a new talent spec from the dictionary provided.
        
        Arguments:
        api -- WoWAPI to fetch glyph item data
        data -- a talent spec dictionary
        
        """
        self._data = data
        #self._api = api
        # Change glyphs around some
        self._glyphs = {}
        for key in self._data['glyphs']:
            glist = []
            for glyph in self._data['glyphs'][key]:
                glist.append(
                        {'id' : glyph['glyph'],
                         'item' : wowthon.Item(api, glyph['item']),
                         'name' : glyph['name'],
                         'icon' : glyph['icon']
                        }
                    )
            self._glyphs.update({key : glist})
        
    @property
    def name(self):
        """Return the name of the spec, e.g. 'Frost'."""
        return self._data['name']
        
    @property
    def selected(self):
        """Return True if the spec is currently selected by the player."""
        return self._data.get('selected', False)
        
    @property
    def icon(self):
        """Return the name of the talent spec's icon."""
        return self._data['icon']
        
    @property
    def build(self):
        """Return a string representing the talent build."""
        return self._data['build']
        
    @property
    def glyphs(self):
        """
        Return a list of dictionaries representing chosen glyphs.
        
        The dicts contain the following keys:
            id -- the glyph's id
            name -- the name of the glyph
            item -- a wowthon.Item representing the glyph item
            icon -- the glyph's icon's name
        
        """
        return self._glyphs
    
    @property
    def trees(self):
        """
        Returns a list of dicts corresponding to the three talent trees
        with the following keys:
        
        total -- the total number of points invested in that tree
        points -- a string representing the distribution of points for
                  the tree
        
        """
        return self._data['trees']