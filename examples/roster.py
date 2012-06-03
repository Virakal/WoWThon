#!/usr/bin/env python3
'''
This example script produces an HTML roster for my guild and prints it to
standard output.

Not pretty, but that's easily fixed. Try
    roster.py > roster.htm
    
to produce an html file.

'''
import wowthon

HTML_PREFIX = '''
<html>
<head>
    <title>Guild Roster</title>
</head>
<body>
<h1>Guild Roster</h1>
<table id="roster">
    <tr class="header">
        <td>Name</td>
        <td>Level</td>
        <td>Rank</td>
        <td>Race</td>
        <td>Class</td>
        <td>Armory Link</td>
    </tr>    
'''

MEMBER_TEMPLATE = '''
<tr>
    <td>{name}</td>
    <td>{level}</td>
    <td>{rank}</td>
    <td>{race}</td>
    <td>{cls}</td>
    <td><a href="{link}">Armory</a></td>
</tr>
'''

HTML_SUFFIX = '''
</table>
</body>
</html>
'''

ARMORY_PREFIX = 'http://eu.battle.net/wow/en/character/draenor/'
ARMORY_SUFFIX = '/advanced'

api = wowthon.WoWAPI('draenor', 'eu')
guild = api.get_guild('delphae')
roster = guild.members
output = HTML_PREFIX
for rank, member in roster:
    name = member.name
    level = member.level
    race = wowthon.RACES[member.race].title()
    cls = wowthon.CLASSES[member.class_].title()
    link = ARMORY_PREFIX + member.name + ARMORY_SUFFIX
    output += MEMBER_TEMPLATE.format(
        name=name,
        level=level,
        race=race,
        cls=cls,
        rank=rank,
        link=link
    )
    
output += HTML_SUFFIX
print(output)