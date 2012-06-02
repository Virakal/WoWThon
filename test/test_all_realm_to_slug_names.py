#! /usr/bin/env python
'''
This script builds a unit test for every realm in every region to ensure that
the static `wowthon.WoWAPI.realm_name_to_slug` method works correctly and is
idempotent.
'''

import unittest
import urllib.request
import json as jsonlib
import wowthon

REGIONS = [
    'http://eu.battle.net/api/wow/',
    'http://us.battle.net/api/wow/',
    'http://kr.battle.net/api/wow/',
    'http://tw.battle.net/api/wow/',
    'http://www.battlenet.com.cn/api/wow/'
]

PATH = 'realm/status'

def ass(p, r):
    # Make an assertion (can't assert in lambdas)
    assert p, r

def _get_data():
    ret = []
    for r in REGIONS:
        url = r + PATH
        req = urllib.request.urlopen(url)
        ret.extend(jsonlib.loads(str(req.read(), 'UTF-8'))['realms'])
    return ret

def addRealmTests():
    i = 0
    realms = _get_data()
    for realm in realms:
        name = realm['name']
        slug = realm['slug']
        # Add normal test
        exec("RealmNameTest.testRealm" + str(i) + \
        " = lambda self: ass(wowthon.WoWAPI.realm_name_to_slug(\"" + name + \
        "\") == \"" + slug + "\", \"" + name + " produced incorrect slug, " + \
        wowthon.WoWAPI.realm_name_to_slug(name) + \
        ", should produce " + slug + "\")")
        
        # Add test to ensure passing the slug through doesn't break it
        exec("RealmNameTest.testSlugPass" + str(i) + \
        " = lambda self: ass(wowthon.WoWAPI.realm_name_to_slug(\"" + slug + \
        "\") == \"" + slug + "\", \"passing slug " + slug +
        " returns incorrect result " + \
        wowthon.WoWAPI.realm_name_to_slug(slug) + "\")")
        
        i += 1
        
class RealmNameTest(unittest.TestCase):        
    def testDummy(self):
        pass
        
if __name__ == '__main__':
    addRealmTests()
    unittest.main()