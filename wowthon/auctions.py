import urllib.request
from urllib.error import HTTPError #, URLError # Need URLError?
import json as jsonlib
import wowthon

class AuctionListings(wowthon._FetchMixin):
    # TODO Do updates and last modified
    #: A list of valid auction house names
    AUCTION_HOUSES = [
        'alliance',
        'horde',
        'neutral'
    ]
    
    #: A list of possible values for time_left
    TIME_LEFT = [
        'VERY_LONG',
        'LONG',
        'SHORT'
    ]
    
    _PATH = 'auction/data/'
    
    def __init__(self, api, realm=None, region=None):
        if not realm:
            realm = api.realm
        if not region:
            region = api.region
        
        self._api = api
        self._realm = realm
        self._region = region
        self._json = None
        self._ah_json = None
        self._url = wowthon.REGION[self._region]['prefix'] + self._PATH \
                    + self._realm
        self._auctions = {}
        self._last_modified = 0
        
    def _get_data(self):
        if not self._ah_json:
            # TODO Check last modified
            # Get the file URL
            url = self._json_property('files')[0]['url']
            # Download the data
            fp = urllib.request.urlopen(url)
            # Read and convert to UTF-8 (json doesn't work on bytes)
            data = fp.readall().decode('utf-8')
            # Interpret the JSON
            self._ah_json = jsonlib.loads(data)
            

    def auctions(self, ah):
        """
        Returns a list of auctions from the sepcified auction house.
        
        Valid auction houses are listed in `AuctionListings.AUCTION_HOUSES`
        
        """
        self._get_data()
        data = self._auctions.get(ah)
        if not data:
            # Auction objects have not yet been built
            auctions = self._ah_json[ah]['auctions']
            data = []
            for auction in auctions:
                data.append(Auction(self._api, auction))
            self._auctions[ah] = data
        return data
        
    def all_auctions(self):
        ret = []
        for ah in AuctionListings.AUCTION_HOUSES:
            ret.extend(self.auctions(ah))
        return ret
        
class Auction:
    """
    Encapsulates an individual auction.
    
    """
    def __init__(self, api, json, realm=None, region=None):
        """
        Creates an auction object from the supplied dictionary
        on the specified realm.
        
        Uses the API's default realm and region if none are specified.
        
        """
        # TODO Test
        # TODO Implement item
        if not realm:
            realm = api.realm
        if not region:
            region = api.region
            
        self._api = api
        self._json = json
        self._realm = realm
        self._region = region
        self._item = None
        self._owner = None
    
    @property
    def id(self):
        """Returns the auction id."""
        return self._json['auc']
        
    @property
    def owner(self):
        """
        Returns a Character object representing the owner of the
        auction.
        
        """
        if not self._owner:
            self._owner = self._api.get_char(
                self._json['owner'],
                self._realm,
                self._region
            )
        return self._owner
        
    @property
    def bid(self):
        """Returns the current bid price on the item."""
        return self._json['bid']
        
    @property
    def buyout(self):
        """
        Returns the buyout price for the item.
        
        Returns X if there is no buyout specified.
        
        """
        # TODO Find out what is returned if there isn't a buyout
        return self._json['buyout']
        
    @property
    def quantity(self):
        """Returns the quanitity of items for sale."""
        return self._json['quantity']
        
    @property
    def item(self):
        """
        Returns an Item object representing the item up for auction.
        
        """
        # TODO Use Item object instead
        if not self_item:
            self._item = self._api.get_item(self._json['item'])
        return self._item
        
    @property
    def time_left(self):
        """
        Returns a string representing the approximate time left on an auction.
        
        """
        return self._json['timeLeft']
        