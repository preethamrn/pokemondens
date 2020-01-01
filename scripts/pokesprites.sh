#!/bin/bash

for i in $(seq -f "%03g" 1 890)
do
  wget "serebii.net/pokedex-swsh/icon/$i.png" 2> /dev/null
  echo "serebii.net/pokedex-swsh/icon/$i.png"
done

