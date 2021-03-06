﻿# WoWthon #
## Overview ##
A wrapper for the [World of Warcraft][wow] [community platform API][api docs]
written in [Python 3][python].

The API should be functional for WoW 4.3.x. A bunch of stuff will likely break
if this version is used after the Mists of Pandaria pre-patch.

The eventual goal is to support all data exposed by Blizzard in some way.
As of 2012-05-23, all data is provided except that listed in the [not yet
implemented][nyi] section below.

[wow]: http://us.battle.net/wow/
[api docs]: http://blizzard.github.com/api-wow-docs/
[python]: http://www.python.org/
[nyi]: #not-yet-implemented

## Features ##
WoWThon attempts to provide a simple and easy to use front end for the CP API.
Data is accessed through object properties and only fetched from the server
when it is actually needed. For the largest part, all interaction with the
server is done behind the scenes.

A caveat of this is that error messages may sometimes be somewhat delayed.

Where possible, every attempt was made to avoid making further lookups from
the server explicitly. For example, the Guild.members property contains not
a list of member IDs but a list of fully functional Character objects.

## Usage ##
WoWthon must be in a folder called `wowthon` and must be in your Python path
or the folder in which your client application resides in order to use the
API. The Python path may be modified using the sys.path variable within
Python.

The module can then be imported using `import wowthon`.

The first step is usually to create a new WoWAPI object. A WoWAPI object
provides a connection point for retrieving data from the Blizzard servers
along with several useful static methods. An API is defined for an individual
realm. To create one for my home realm:

    api = wowthon.WoWAPI('Draenor', 'eu')

We can then use the WoWAPI object to grab guilds, characters, etc. from the
server.

    # Grab my guild!
    delphae = api.get_guild('Delphae')

    # or my druid :)
    bush = api.get_char('untamedbush')

and we can then treat these objects in a fairly intuitive manner.

    delphae.level
    > 25

    # wowthon.CLASSES maps class ids to their English names
    wowthon.CLASSES[bush.class_]
    > 'druid'

A more complete documentation will be written soon. Additional help can be
found in the class and method docstrings.

## Requirements ##
WoWthon requires Python 3 and has been tested on CPython 3.2.2.

The following modules are required, supplied with the standard
Python distribution:

- `urllib`
- `json`
- `base64`
- `time`
- `hashlib`
- `hmac`

Applications naturally require a functional internet connection to obtain
data from the Blizzard servers and are also bound by the community platform
API's [usage policy][usage].

[usage]: http://blizzard.github.com/api-wow-docs/#idp26536

## Future ##
The following is a list of features and improvements still to be made:

- More effcient bandwidth and API credit usage
- Improved documentation, especially at class level, will provide
  tutorial-style guidance
- Deal with characters under level 10 in some way, can appear in guild
  listings but can't be directly accessed
- Eventually replace most or all dicts with objects
- Wowhead integration for data not exposed by Blizzard (particularly spells)
- More examples
- Method of installation (setuptools or similar)

## Not Yet Implemented ##
The following is a list of features not yet implemented:

- Items:
    - Source lookup
    - Mutability (reforge(), socket())?
    - Possibly missed some some item fields?

- Guild:
    - *The following are currently exposed as raw dictionaries*:
        - Guild achievements
        - Guild perks
        - Guild rewards
    - Guild emblem rendering

- PvP:
    - Ladders

- Characters:
    - Feed
    - Items
    - Reputation
    - Achievements
    - Progression

- Data (List all):
    - Achievements
    - Guild Achievements
    - Guild Perks
    - Guild Rewards
    - Recipes (Add to character professions too)

## Copyright and License ##
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">
<img alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" />
</a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">
WoWthon</span> by <span xmlns:cc="http://creativecommons.org/ns#"
property="cc:attributionName">Jonathan Goodger</span> is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">
Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.
No warranty is supplied with this product.

Note: Derivative works and API consumers are also bound by
[Blizzard's API policy][api policy].

Copyright © 2012 Jonathan Goodger

[api policy]: http://blizzard.github.com/api-wow-docs/#idp56608
