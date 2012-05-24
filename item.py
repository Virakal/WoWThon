# TODO Currently a dummy
import wowthon

class Item(wowthon._FetchMixin):
    def __init__(self, api, id):
        self._api = api
        self._id = id