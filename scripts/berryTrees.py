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

allBerries = {}

# NOTE: route 3 has a bug that mentions persimberry twice
def getBerries(berries):
    text = berries.text.replace('Berry', '').strip()
    text.replace('\r', '')
    text.replace('\n', '')
    berries = []
    for berry in text.split(' '):
        berryID = berry.lower()+('berry' if berry.lower() != 'leftovers' else '')
        berries.append(berryID)
        allBerries[berryID] = berry + (' Berry' if berry.lower() != 'leftovers' else '')
    return berries

def getPokemon(pokemon):
    pokemonList = pokemon.findAll('a')
    pokemonList = list(pokemon.text.strip().lower() for pokemon in pokemonList)
    result = []
    for item in pokemonList:
        if item == 'skowvet':
            result.append('819')
        elif item == 'skwovet':
            result.append('819')
        elif item == 'greedent':
            result.append('819')
        elif item == 'cherubi':
            result.append('420')
        else:
            raise Exception('uncaught pokemon: ' + item)
    return result

def getTreeName(info):
    a = info.find('a')
    return {
        'name': a.text,
        'link': 'https://www.serebii.net' + a.get('href')
    }

def fitness(berry):
    return berry['id']

if __name__ == '__main__':
    r = requests.get('https://www.serebii.net/swordshield/berrytrees.shtml')
    soup = BeautifulSoup(r.text, features='html.parser')

    rows = soup.findAll('tr')

    for row in rows:
        children = row.findAll('td', class_='fooinfo') # get all 4 columns of the row
        if len(children) != 4:
            continue # some of the rows are just information panels without pokemon
        [img, info, berries, pokemon] = children
        information = getTreeName(info)
        if 'Route' in information['name']:
            continue
        print({'info': information, 'berries': getBerries(berries), 'pokemon': getPokemon(pokemon), 'img': 'https://www.serebii.net/swordshield/' + img.find('img').get('src'), 'position': {'x': 0, 'y': 0}})
    
    searchBerries = []
    for k, v in allBerries.items():
        searchBerries.append({'id': k, 'name': v})
    searchBerries = sorted(searchBerries, key=fitness)
    print(searchBerries)

# s/'([^']*?)':/$1:/
# s/\}\}, /}},/