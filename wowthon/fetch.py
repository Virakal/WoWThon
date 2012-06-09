import urllib.request
from urllib.error import HTTPError #, URLError # Need URLError?

class _FetchMixin:
    """
    Mixin class to define common behaviour for any object that fetches data.
    
    """
    def _fetch(self, force=False):
        """
        Fetch the data from the WoW server if it has not already been
        downloaded.
        
        Arguments:
        force -- if true, fetches data regardless of whether the data
                 already exists.
        
        """
        # TODO Use last modified to refresh
        if force or not self._json:
            self._json = self._api._get_json(self._url)
            # Try to update last modified if it exists
            try:
                self._last_modified = self._json['lastModified']
            except KeyError:
                pass
            
    def force_update(self):
        """Force the data to update itself from the server."""
        self._fetch(force=True)
        
    def _json_property(self, name):
        """
        Get the property from the JSON object with the name `name`.
        
        Fetches the data from the server if necessary. This method will update
        the object's requested fields if necessary to retrieve the data asked
        of it. After requesting optional data, this data will be fetched with
        every subsequent update.
        
        """
        try:
            # Check if object has a _fields property
            self._fields
            has_fields = True
        except AttributeError:
            has_fields = False
            
        self._fetch()
        try:
            return self._json[name]
        except KeyError:
            if has_fields and name in self._fields:
                # If we don't have it, but we should have it, we force update
                self.force_update()
                return self._json[name]
            else:
                # Otherwise, we don't know what it is
                raise
                
    def _add_field(self, name):
        """
        Add a field to the list of fields fetched.
        
        """
        if name not in self._fields:
            self._fields.append(name)
            self._url = self._generate_url()