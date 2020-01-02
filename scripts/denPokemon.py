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

# ASSUMPTIONS: each version has 12 Pokemon per raid => first 12 images for Sword, next 12 images for Shield
# error if there are more than 24 Pokemon => something in the website changed.
# solution: potentially use the rowspan of the Sword/Shield td element and more carefully navigate the table.
def getPokemon(raid):
    allPokemon = raid.findAll('img')
    # pre validation
    if len(allPokemon) != 24:
        raise Exception('Invalid number of Pokemon in this raid')

    raidPokemon = {'sword': [], 'shield': []}
    for index, pokemon in enumerate(allPokemon):
        version = 'sword'
        if index >= 12:
            version = 'shield'
        imgSrc = pokemon.get('src')
        m = re.search('/pokedex-swsh/icon/(.+?).png', imgSrc)
        if m:
            pokeID = m.group(1)
            raidPokemon[version].append(pokeID)

    # post validation
    if len(raidPokemon['sword']) != 12 or len(raidPokemon['shield']) != 12:
        raise Exception('Invalid number of Pokemon in one of the versions: ' + raidPokemon)
    
    return raidPokemon

def getDenNumber(raid):
    a = raid.find('a')
    return {
        'number': a.text,
        'link': a.get('href')
    }

if __name__ == '__main__':
    r = requests.get('https://www.serebii.net/swordshield/maxraidbattledens.shtml')
    soup = BeautifulSoup(r.text, features='html.parser')

    rows = soup.findAll('tr')

    for row in rows:
        children = row.findAll('td', class_='picturetd') # get all 4 columns of the row
        if len(children) != 4:
            continue # some of the rows are just information panels without pokemon
        [loc, img, common, rare] = children

        print(loc.text)
        print('https://www.serebii.net/' + img.find('a').get('href'))
        print({**getDenNumber(common), **getPokemon(common)})
        print({**getDenNumber(rare), **getPokemon(rare)})
        print()