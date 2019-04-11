import wowthon

class Guild(wowthon._FetchMixin):
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
                 initial_fields=None, json=None):
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
        json -- set this to construct the guild from previously fetched json

        """
        # TODO self.guild_rank(Character/Name)
        if not realm: realm = api.realm
        if not region: region = api.region
        if not initial_fields: initial_fields = []
        if type(realm) == wowthon.Realm:
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

        return wowthon.REGION[self._region]['prefix'] + self._PATH + \
               self._realm + '/' + self._name + fields

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
            char = self._api.get_char(
                                      member['character']['name'],
                                      self.realm,
                                      self.region,
                                      json=member['character']
                                     )
            #char._g_rank = member['rank']
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
