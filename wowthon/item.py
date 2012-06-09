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
    
    SOCKET_TYPES = [
        'RED',
        'YELLOW',
        'BLUE',
        'META',
        'PRISMATIC',
        'COGWHEEL',
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
        self._region = region
        self._locale = locale
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + \
                    str(id) + '?locale=' + locale
        
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
        
    @property
    def min_faction_id(self):
        """
        Returns the id of the faction required to use the item.
        
        Returns 0 if the item is not restricted by faction.
        
        See also:
        `Item.min_reputation`
        
        """
        return self._json_property('minFactionId')
        
    @property
    def min_reputation(self):
        """
        Return the minimum reputation level required to use the item.
        
        This is represented by an integer. A map of integers to their English
        equivalents can be found at `wowthon.FACTION_LEVELS`.
        
        Returns 0 if the item is not restricted by faction.
        
        See also:
        `Item.min_faction_id`
        
        """
        return self._json_property('minReputation')
        
    @property
    def quality(self):
        """
        Returns an integer representing the item's quality, that is, whether
        an item is epic, legendary, or so on.
        
        A map of the identifiers to their English equivalents may be found in
        `wowthon.ITEM_QUALITY`.
        
        """
        return self._json_property('quality')
        
    @property
    def sell_price(self):
        """
        Returns the sell price, or vendor price, of the item.
        
        Returns 0 if the item cannot be sold to a vendor.
        
        """
        return self._json_property('sellPrice')
        
    @property
    def required_skill(self):
        """
        Returns an id representing the required profession for using the item.
        
        Returns 0 if a profession is not required.
        
        See also: `Item.required_skill_rank`
        
        """
        return self._json_property('requiredSkill')
       
    @property
    def required_level(self):
        """
        Return the minimum required character level to use the item.
        
        Returns 0 if the item is not limited.
        
        """
        return self._json_property('requiredLevel')
        
    @property
    def required_skill_rank(self):
        """
        Returns the minimum profession level, or rank, required to use the
        item.
        
        Returns 0 if a profession is not required.
        
        See also: `Item.required_skill`
        
        """
        return self._json_property('requiredSkillRank')
        
    @property
    def base_armor(self):
        """
        Return the base armor of the item.
        
        This will be the same as `Item.armor` unless the item has bonus armor,
        in which case `Item.armor` will be higher.
        
        Returns 0 if the item provides no armor.
        
        See also:
        `Item.armor`,
        `Item.bonus_armor`
        
        """
        return self._json_property('baseArmor')
        
    @property
    def has_sockets(self):
        """
        Returns True if the item has sockets, for gems or cogwheels.
        
        See also:
        `Item.socket_info`
        
        """
        return self._json_property('hasSockets')
        
    @property
    def socket_info(self):
        """
        Returns information on the item's sockets as a dictionary.
        
        The dictionary has two fields:
        sockets -- a list of socket identifiers
        bonus -- a description of the socket bonus
        
        Possible socket identifiers are listed in `Item.SOCKET_TYPES`
        
        Returns None if the item has no sockets.
        
        See also:
        `Item.has_sockets`
        
        """
        try:
            data = self._json_property('socketInfo')
        except KeyError:
            # No sockets
            return None
            
        bonus = data['socketBonus']
        sockets = []
        for socket in data['sockets']:
            sockets.append(socket['type'])
            
        ret = {
            'sockets' : sockets,
            'bonus' : bonus
        }
        
        return ret
        
    @property
    def auctionable(self):
        """
        Returns True if the item may be placed on an Auction House.
        
        """
        return self._json_property('isAuctionable')
        
    @property
    def armor(self):
        """
        Returns the armor value of the item.
        
        If the item has no bonus armor, this value will be equal to
        `Item.base_armor`, otherwise, this value will be the higher.
        
        Returns 0 if the item does not provide armor.
        
        See also:
        `Item.base_armor`,
        `Item.bonus_armor`
        
        """
        return self._json_property('armor')
        
    @property
    def bonus_armor(self):
        """
        Returns the bonus armor value of the item.
        
        This is the amount of "extra" armor the item has.
        
        Returns 0 if the item does not provide armor or has no bonus armor.
        
        See also:
        `Item.base_armor`,
        `Item.armor`
        
        """
        return self.armor - self.base_armor
        
    @property
    def display_info_id(self):
        """
        Returns an id number representing the item's model and skin.
        
        """
        return self._json_property('displayInfoId')
        
    @property
    def disenchanting_rank(self):
        """
        Return the minimum enchanting skill required to disenchant the item.
        
        Returns None if the item can not be disenchanted.
        
        """
        try:
            return self._json_property('disenchantingSkillRank')
        except KeyError:
            return None
            
    @property
    def source(self):
        """
        Returns a dictionary detailing an item's source.
        
        The dictionary has two fields:
        id -- the source's id
        type -- the source type (e.g. "CREATED_BY_SPELL")
        
        """
        data = self._json_property('itemSource')
        ret = {
            'id' : data['sourceId'],
            'type' : data['sourceType']
        }
        return ret
        
    @property
    def required_ability(self):
        """
        Returns a dictionary detailing the ability required to use the item.
        
        The dictionary has the following fields:
        id -- the spell id for the ability
        name -- the name of the ability
        description -- a description of the ability
        
        Returns None if the item does not have a required ability.
        
        See also:
        `Item.required_skill`
        
        """
        try:
            data = self._json_property('requiredAbility')
        except KeyError:
            return None
        
        ret = {
            'id' : data['spellId'],
            'name' : data['name'],
            'description' : data['description']
        }
        
        return ret
        
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
        
class ItemSet(wowthon._FetchMixin):
    """
    Encapsulates an item set.
    
    """
    
    _PATH = 'item/set/'
    
    def __init__(self, api, id, region=None, locale=None, json=None):
        """
        Creates a new item set.
        
        Arguments:
        api -- the WoWAPI instance to use
        id -- the set id
        
        Optional Arguments:
        region -- the region to use for the data (default: api setting)
        locale -- the locale to use for the data (default: api setting)
        json -- a prebuilt dictionary to collect data from (default: None)
        
        """
        if not region: region = api.region
        if not locale: locale = api.locale
        self._api = api
        self._id = id
        self._region = region
        self._locale = locale
        self._json = json
        self._url = wowthon.REGION[region]['prefix'] + self._PATH + str(id)
        
    @property
    def id(self):
        """
        Return the item set's id.
        
        """
        return self._id
        
    @property
    def region(self):
        """
        Return the region code the item set uses.
        
        """
        return self._region
        
    @property
    def locale(self):
        """
        Return the locale of the item.
        
        """
        return self._locale
        
    @property
    def name(self):
        """
        Return the name of the item set.
        
        """
        return self._json_property('name')
        
    @property
    def bonuses(self):
        """
        Return a list of dictionaries defining the set bonuses.
        The dictionaries have the following fields:
        
        description -- a description of the bonus conferred
        threshold -- the number of items required to confer the bonus
        
        """
        return self._json_property('setBonuses')
        
    def bonuses_with_items(self, count):
        """
        Returns a list of all bonuses conferred with `count` number of items
        from the set equipped.
        
        Returns an empty list if no bonuses are given.
        
        """
        return [x for x in self.bonuses if x['threshold'] <= count]