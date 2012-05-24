# WoWthon #
## Overview ##
A wrapper for the [WoW community API][api docs] written in [Python 3][python].

The API should be functional for WoW 4.3.x. A bunch of stuff will likely break
if this version is used after the Mists of Pandaria pre-patch.

The eventual goal is to support all data exposed by Blizzard in some way.
As of 2012-05-23, all data is provided except that listed in the [not yet
implemented][nyi] section below.

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
The WoWthon folder must be in your system path or the folder in which your
client application resides in order to use the API. The system path may be
modified using the sys.path variable within Python.

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

## Todo ##
The following is a list of tasks still to be done, or considered:

- More comprehensive testing (many unit tests lost)
- 'Last modified' checking
- Method of installing
- Exceptions and error code handling
- Authentication
- Implement locales (find out what does and doesn't need locale)
- Improve documentation, especially at class level, provide
  tutorial-style guidance.
- Deal with characters under level 10 in some way, can appear in guild
  listings but can't be directly accessed
- Considering moving the constants to API methods, or moving the
  API's static methods out in to the wowthon package
- Caching of results and other peformance boosts
- Eventually replace most or all dicts with objects?
- Wowhead integration for data not exposed by Blizzard (particularly spells)
- Add more examples

## Not Yet Implemented ##
The following is a list of features not yet implemented:

- API:
    - Error code handling
    - Exceptions
    - Localisation
    - Authentication

- Items:
    - All

- Achievements:
    - All

- Guild:
    - Guild achievements
    - Guild perks
    - Guild rewards

- PvP:
    - All

- Characters:
    - Feed
    - Items
    - Reputation
    - Companions
    - Pets
    - Achievements
    - Progression

- Data (List all):
    - Battlegroups
    - Classes (*currently hardcoded*)
    - Races (*currently hardcoded*)
    - Achievements
    - Guild Achievements
    - Guild Perks
    - Guild Rewards
    - Item Classes
    
## Copyright and License ##
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">
<img alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" />
</a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">
WoWthon</span> by <span xmlns:cc="http://creativecommons.org/ns#" 
property="cc:attributionName">Jonathan Goodger</span> is licensed under a 
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/">
Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.

Note: Derivative works and API consumers are also bound by
 [Blizzard's API policy][api policy]

Copyright © 2012 Jonathan Goodger

[api policy]: http://blizzard.github.com/api-wow-docs/#idp56608