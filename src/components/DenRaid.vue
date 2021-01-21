<template>
  <div class='den-raid'>
    <a class='name' :href='link'>{{name}} - {{type}}</a>
    <div class='sw version'>Sword</div>
    <div class='swp pokemon-list'>
      <img v-for='(pokeID, index) in swordPokemon' :key='index' :src='`${publicPath}sprites/${pokeID}.png`' />
    </div>
    <div class='sh version'>Shield</div>
    <div class='shp pokemon-list'>
      <img v-for='(pokeID, index) in shieldPokemon' :key='index' :src='`${publicPath}sprites/${pokeID}.png`' />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DenRaid',
  data() {
    return {
      publicPath: process.env.VUE_APP_PUBLIC_PATH,
    }
  },
  props: {
    name: String,
    type: String,
    link: String,
    swordPokemon: Array,
    shieldPokemon: Array,
  },
}
</script>

<style scoped>
.sw { background-color: #00d1f6; color: #002b33; }
.swp { background-color: #ccf7ff; }

.sh { background-color: #9e2306; color: #190501; }
.shp { background-color: #fdd6ce; }

.name {
  justify-self: center;
  color: #000;
  font-weight: 600;
  padding-bottom: 10px;
}
.version {
  line-height: 100%;
  font-weight: 600;
  padding: 10px;
}
.den-raid {
  background-color: #ffffff;
  padding: 5px;
  display: grid;
  grid-template:
    "name" 1fr
    "sw swp" auto
    "sh shp" auto / 1fr 5fr;
}
.pokemon-list {
  display: grid;
  grid: repeat(3, 50px) / auto-flow 60px;
}
</style>
