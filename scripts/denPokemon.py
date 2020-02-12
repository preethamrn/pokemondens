#!/bin/python

"""
Install dependencies:
pip install requests
pip install bs4
pip install re
"""

import requests
import re
from bs4 import BeautifulSoup

allPokemonIDs = {}

# ASSUMPTIONS: each version has 12 Pokemon per raid => first 12 images for Sword, next 12 images for Shield
# error if there are more than 24 Pokemon => something in the website changed.
# solution: potentially use the rowspan of the Sword/Shield td element and more carefully navigate the table.
def getPokemon(raid):
    allPokemon = raid.findAll('img')
    # pre validation
    if len(allPokemon) != 24:
        raise Exception('Invalid number of Pokemon in this raid')

    raidPokemon = {'swordPokemon': [], 'shieldPokemon': []}
    for index, pokemon in enumerate(allPokemon):
        version = 'swordPokemon'
        if index >= 12:
            version = 'shieldPokemon'
        imgSrc = pokemon.get('src')
        imgAlt = pokemon.get('alt')
        m = re.search('/pokedex-swsh/icon/(.+?).png', imgSrc)
        if m:
            pokeID = m.group(1)
            raidPokemon[version].append(pokeID)
            m2 = re.search('(.+?) -.*', imgAlt)
            if m2:
                pokeName = m2.group(1)
                allPokemonIDs[pokeID] = pokeName

    # post validation
    if len(raidPokemon['swordPokemon']) != 12 or len(raidPokemon['shieldPokemon']) != 12:
        raise Exception('Invalid number of Pokemon in one of the versions: ' + raidPokemon)

    return raidPokemon

def getDenNumber(raid):
    a = raid.find('a')
    return {
        'name': a.text,
        'link': 'https://www.serebii.net/swordshield/' + a.get('href')
    }

def getFullPokemonName(id, name):
    if name == 'Rotom':
        if id.endswith('-m'):
            return {'id': id, 'name': 'Mow Rotom'}
        if id.endswith('-w'):
            return {'id': id, 'name': 'Wash Rotom'}
        if id.endswith('-h'):
            return {'id': id, 'name': 'Heat Rotom'}
        if id.endswith('-f'):
            return {'id': id, 'name': 'Frost Rotom'}
        if id.endswith('-s'):
            return {'id': id, 'name': 'Fan Rotom'}
    if id.endswith('-g'):
        return {'id': id, 'name': 'Galarian ' + name}
    if id.endswith('-a'):
        return {'id': id, 'name': 'Galarian ' + name}
    elif id.endswith('-gi'):
        return {'id': id, 'name': 'Gigantamax ' + name}
    elif id.endswith('-e'):
        return {'id': id, 'name': name + ' East'}
    elif id.endswith('-w'):
        return {'id': id, 'name': name + ' West'}
    elif id.endswith('-f'):
        return {'id': id, 'name': 'Female ' + name}
    elif id.endswith('-m'):
        return {'id': id, 'name': 'Male ' + name}
    elif '-' in id:
        raise Exception("unknown id format: " + id)
    else:
        # return None  # uncomment if we want only the special Pokemon
        return {'id': id, 'name': name} # returns all Pokemon found in dens

def fitness(pokemon):
    return pokemon['id']

if __name__ == '__main__':
    r = requests.get('https://www.serebii.net/swordshield/maxraidbattledens.shtml')
    soup = BeautifulSoup(r.text, features='html.parser')

    allDens = {}

    rows = soup.findAll('tr')

    for row in rows:
        children = row.findAll('td', class_='picturetd') # get all 4 columns of the row
        if len(children) != 4:
            continue # some of the rows are just information panels without pokemon
        [loc, img, common, rare] = children

        commonDenNumber = getDenNumber(common)
        rareDenNumber = getDenNumber(rare)
        m1 = re.search('Den (.+?)$', commonDenNumber['name'])
        m2 = re.search('Den (.+?)$', rareDenNumber['name'])
        commonID = m1.group(1)
        rareID = m2.group(1)
        print({'location': loc.text, 'img': 'https://www.serebii.net/swordshield/' + img.find('img').get('src'), 'commonID': commonID, 'rareID': rareID, 'position': {'x': 0, 'y': 0}})
        allDens[commonID] = {**commonDenNumber, **getPokemon(common)}
        allDens[rareID] = {**rareDenNumber, **getPokemon(rare)}

    print(allDens)

    fullPokemonNames = []
    for id, name in allPokemonIDs.items():
        fullName = getFullPokemonName(id, name)
        if fullName:
            fullPokemonNames.append(fullName)

    fullPokemonNames = sorted(fullPokemonNames, key=fitness)
    print(fullPokemonNames)

# s/\{'location': (.*?), 'img': (.*?), 'commonID': '(.*?)', 'rareID': '(.*?)', 'position': (.*)$/{location: $1, img: $2, commonID: $3, rareID: $4, position: $5,/
# s/\{'x': 0, 'y': 0\}/{x: 0, y: 0}/
# s/'([^']*?)':/$1:/
# s/'\]\}, /']},\n/