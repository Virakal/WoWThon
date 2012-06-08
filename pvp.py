import wowthon

class ArenaTeam(wowthon._FetchMixin):
    """
    Encapsulates an arena team.
    
    """
    
    _PATH = 'arena/'
    
    def __init__(self, api, size, name, realm=None, region=None,
                 locale=None, json=None):
        """
        Create a new ArenaTeam object.
        
        The team size can be an integer, e.g. 2, or a string, e.g. "2v2".
        Valid team sizes may be found in `wowthon.TEAM_SIZES`.
        
        `realm` may be a realm object, a realm name or a realm slug.
        
        Arguments:
        api -- the WoWAPI instance to use
        size -- the team size
        name -- the name of the team
        
        Optional arguments:
        realm -- the realm the team resides on (default: api default)
        region -- the API region to use (default: api default)
        locale -- the locale to use (default: api default)
        json -- a dictionary to use instead of fetching from the server
                (default: None)
        
        """
        if not realm: realm = api.realm
        if not region: region = api.region
        if not locale: locale = api.locale
        if isinstance(realm, str): realm = api.get_realm(realm)[0]
        if isinstance(size, int): size = wowthon.TEAM_SIZES[size]
        
        self._api = api
        self._name = name
        self._size = size
        self._json = json
        self._realm = realm
        self._region = region
        self._locale = locale
        
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + \
                        self._realm.slug + '/' + self._size + '/' + \
                        self._name
        
    @property
    def realm(self):
        """
        Return a `wowthon.Realm` object for the realm the team resides on.
        
        """
        return self._realm
        
    @property
    def region(self):
        """Return the name of the region the team resides on."""
        return self._region
        
    @property
    def locale(self):
        """Returns the code for the locale the information is in."""
        return self._locale
        
    @property
    def name(self):
        """Returns the name of the team."""
        return self._name
        
    @property
    def rating(self):
        """Returns the team's matchmaking rating."""
        return self._json_property('rating')
        
    @property
    def ranking(self):
        """
        Returns the team's ladder ranking.
        
        Returns 0 if the team is not ranked.
        
        """
        return self._json_property('ranking')
        
    @property
    def team_size(self):
        """
        Returns an integer representing the team size.
        
        For example, a 3v3 team returns 3.
        
        See also:
        `wowthon.TEAM_SIZES`
        
        """
        return self._json_property('teamsize')
        
    @property
    def created(self):
        """
        Returns a string containing the date the team was created, in
        YYYY-MM-DD format.
        
        """
        return self._json_property('created')
        
    @property
    def games_played(self):
        """
        Return the number of games played by the team in the current week.
        
        """
        return self._json_property('gamesPlayed')
        
    @property
    def games_won(self):
        """
        Return the number of games won by the team in the current week.
        
        """
        return self._json_property('gamesWon')
        
    @property
    def games_lost(self):
        """
        Return the number of games lost by the team in the current week.
        
        """
        return self._json_property('gamesLost')
        
    @property
    def season_games_played(self):
        """
        Return the number of games played by the team in the current season.
        
        """
        return self._json_property('sessionGamesPlayed')
        
    @property
    def season_games_won(self):
        """
        Return the number of games won by the team in the current season.
        
        """
        return self._json_property('sessionGamesWon')
        
    @property
    def season_games_lost(self):
        """
        Return the number of games lost by the team in the current season.
        
        """
        return self._json_property('sessionGamesLost')
        
    @property
    def last_season_ranking(self):
        """
        Return the team's ranking for the last season.
        
        Returns 0 if the team was unranked or non-existent last season.
        
        """
        return self._json_property('lastSessionRanking')
        
    @property
    def side(self):
        """
        Returns the id for the faction the team plays for.
        
        e.g. 1 for a Horde team.
        
        """
        side = self._json_property('side')
        # NOTE locale will be a pain here
        assert side in ['horde', 'alliance'], "unusual side returned"
        
        return 1 if side == 'horde' else 0
        
    @property
    def current_week_ranking(self):
        """
        Returns the team's ranking for the current week.
        
        """
        return self._json_property('currentWeekRanking')
        
    @property
    def members(self):
        """
        Return a list of dictionaries describing the team's members.
        
        The dictionary has the following fields:
        
        character -- a `wowthon.Character` object representing the member
        rank -- the player's rank
        games_played -- the number of games played this week by the member
        games_won -- the number of games won this week by the member
        games_lost -- the number of games lost this week by the member
        season_games_played -- the number of games played this season by the
                               member
        season_games_won -- the number of games won this season by the member
        season_games_lost -- the number of games lost this season by the
                             member
        rating -- the player's personal rating
        
        """
        data = self._json_property('members')
        ret = []
        for player in data:
            member = {
                'character' : self._api.get_char(
                                   player['character']['name'],
                                   json=player
                              ),
                'rank' : player['rank'],
                'games_played' : player['gamesPlayed'],
                'games_won' : player['gamesWon'],
                'games_lost' : player['gamesLost'],
                'season_games_played' : player['sessionGamesPlayed'],
                'season_games_won' : player['sessionGamesWon'],
                'season_games_lost' : player['sessionGamesLost'],
                'rating' : player['personalRating']
            }
            ret.append(member)
            
        return ret