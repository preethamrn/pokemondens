#!/bin/python

import requests
import re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    r = requests.get('https://www.serebii.net/pokemon/all.shtml')
    soup = BeautifulSoup(r.text, features='html.parser')

    allPokemon = []

    rows = soup.findAll('tr')

    for row in rows:
        children = row.findAll('td', class_='fooinfo') # get all columns of the row
        if len(children) != 11:
            continue # some of the rows are just information panels without pokemon
        numHTML = children[0].text
        nameHTML = children[2].text
        m1 = re.search('\s*#(.+)\r\s*', numHTML)
        pokeID = m1.group(1)
        m2 = re.search('\s*(.+)\s*', nameHTML)
        pokeName = m2.group(1)

        allPokemon.append({'id': pokeID, 'name': pokeName})

    print(allPokemon)

# s/'id': u'(.*?)', 'name': u'(.*?)'/id: '$1', name: '$2'/g