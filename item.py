import wowthon

class Item(wowthon._FetchMixin):
    """
    Encapsulates a WoW item.
    
    """
    _PATH = 'item/'
    
    TRIGGERS = [
        'ON_USE',
        'ON_EQUIP'
    ]
    
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
        
    @property
    def item_spells(self):
        """
        Returns a list of dictionaries detailing spells associated with the
        item. These are the item's "on use" or "on equip" effects.
        
        The dictionary has the following fields:
        id -- the spell id
        charges -- the number of charges the item has
        consumable -- True if the item is consumed when the charges expire
        category -- a spell category id
        trigger -- when the spell is triggered (possible values can be found
                   in Item.TRIGGERS)
                   
        along with possibly a spell field containing a dict with the following
        fields:
        id -- the spell id
        name -- the spell name
        icon -- the spell icon
        description -- a spell description
        cast_time (optional) -- a string identifying the cast time
        cooldown (optional) -- a string describing the spell cooldown
        
        Note: spell will likely be rplaced with a Spell object when the spell
        API is released.
        
        """
        spells = self._json_property('itemSpells')
        ret = []
        for spell in spells:
            pyspell = {
                'id' : spell['spellId'],
                'charges' : spell['nCharges'],
                'consumable' : spell['consumable'],
                'category' : spell['categoryId'],
                'trigger' : spell['trigger']
            }
            # Add spell if it exists
            try:
                sfield = spell['spell']
                pysfield = {
                    'id' : sfield['id'],
                    'name' : sfield['name'],
                    'icon' : sfield['icon'],
                    'description' : sfield['description']
                }
                cast_time = sfield.get('castTime', None)
                cooldown = sfield.get('cooldown', None)
                if cast_time:
                    # Cast time exists, add that
                    pysfield.update({'cast_time' : cast_time})
                if cooldown:
                    # Cooldown exists, add that
                    pysfield.update({'cooldown' : cooldown})
                pyspell.update({'spell' : pysfield})
            except KeyError:
                # No spell field
                pass
            ret.append(pyspell)
        return ret
        
    @property
    def buy_price(self):
        """
        Return the purchase brice for the item from the vendor.
        
        """
        return self._json_property('buyPrice')
        
    @property
    def item_class(self):
        """
        Return the class id of the item.
        
        """
        return self._json_property('itemClass')
        
    @property
    def item_subclass(self):
        """
        Return the subclass id of the item.
        
        """
        return self._json_property('itemSubClass')
        
    @property
    def container_slots(self):
        """
        Return the number of slots a container has.
        
        Returns 0 if the item is not a container.
        
        """
        return self._json_property('containerSlots')
        
    @property
    def container(self):
        """
        Returns True if the item is a container (e.g. a bag).
        
        """
        return True if self.container_slots else False
        
    @property
    def weapon_info(self):
        """
        Return a dictionary describing the weapon information for an item.
        
        Returns None if the item is not a weapon.
        
        The dictionary has the following fields:
        min_damage -- the weapon's minimum damage
        max_damage -- the weapon's maximum damage
        speed -- the weapon's attack speed
        dps -- the weapon's damage per second
        
        """
        try:
            data = self._json_property('weaponInfo')
        except KeyError:
            return None
        ret = {
            'min_damage' : data['damage']['min'],
            'max_damage' : data['damage']['max'],
            'speed' : data['weaponSpeed'],
            'dps' : data['dps'],
        }
        return ret
        
    @property
    def inventory_type(self):
        """
        Returns the inventory type id for the item.
        
        """
        return self._json_property('inventoryType')
        
    @property
    def equippable(self):
        """
        Returns True if the item is equippable.
        
        """
        return self._json_property('equippable')
    
    @property
    def item_level(self):
        """
        Return the item's item level or ilevel.
        
        """
        return self._json_property('itemLevel')
        
    @property
    def max_count(self):
        """
        Return the maximum number of items that may exist in an inventory
        at any one time.
        
        Returns 0 if there is no limit.
        
        """
        return self._json_property('maxCount')
        
    @property
    def max_durability(self):
        """
        Returns the maximum durability level of an object.
        
        Returns 0 if the item does not have durability.
        
        """
        return self._json_property('maxDurability')
    
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
        