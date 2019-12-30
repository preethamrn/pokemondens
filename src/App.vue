<template>
  <div id="app">
    <img alt="Pokemon Wild Area Map" src="./assets/pokemon-wild-area.jpg">
    <DenLocation v-for="(den, index) in dens" :key="index" :position='den.position' :gmax='denPokemon[den.id].gmax' />
  </div>
</template>

<script>
import DenLocation from './components/DenLocation.vue'

export default {
  name: 'app',
  components: {
    DenLocation
  },
  data() {
    return {
      dens: [
        {id: 1, position: {x: 10, y: 100}},
        {id: 27, position: {x: 500, y: 1000}},
      ],
      denPokemon: {
        1: {gmax: false, pokemon: [101]},
        27: {gmax: true, pokemon: [207]},
      },
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
