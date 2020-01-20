#!/usr/bin/env sh

# abort on errors
set -e

# build
npm run build

# navigate into the build output directory
cd dist

echo 'www.pokemondens.com' > CNAME

git init
git add -A
git commit -m "deploy $1" 
git config --local credential.helper ""

git push -f https://github.com/pokemondenmap/pokemondenmap.github.io master

cd -
