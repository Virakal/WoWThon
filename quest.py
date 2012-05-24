# TODO Currently a dummy
import wowthon

class Quest(wowthon._FetchMixin):
    def __init__(self, api, id):
        self._api = api
        self._id = id