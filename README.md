# PokemonDenMap
Map of all the dens with den numbers and list of Pokemon available in Pokemon Sword/Shield

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your tests
```
npm run test
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# TODO
- Setup all den Pokemon (update denPokemon.py script to generate the required component data)
- Setup all den positions
- Fix the transform-origin for scaling (it doesn't feel like the natural center of the screen is being preserved)
- Fix styling for the hover layout
- Add deep links into Serebii
- Add contact and credits links
- Search for dens by Pokemon
- Add other map elements (trees, items, nursery, watts trader, digging duo) + toggle map elements functionality
- Scale map and center the transform to browser width on page load (only once!)

# DONE
- Map with den markers positioning functionality
- Add hover to show Pokemon functionality
- Show Pokemon icons (download sprites from Serebii)
- Add list of all pokemon to each den (from Serebii)
- Support list of Pokemon in a table
- Draggable map (handleDrag can also update all the den location positions): https://vuejsexamples.com/a-vue-component-that-create-moveable-and-resizable/
- Resize buttons on map (change the scale)
