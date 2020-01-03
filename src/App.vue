<template>
  <div id="app">
    <img alt="Pokemon Wild Area Map" src="./assets/pokemon-wild-area.png">
    <DenLocation v-for="(den, index) in dens" :key="index" :position='den.position' :commonDen='denPokemon[den.commonID]' :rareDen='denPokemon[den.rareID]' :gmax='denPokemon[den.commonID].gmax || denPokemon[den.rareID].gmax' :screenshotImg='den.img'/>
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
        {commonID: 38, rareID: 64, location: "Axew's Eye", img: "https://www.serebii.net/swordshield/den/th/axew'seye-1.jpg",  position: {x: 10, y: 100}},
      ],
      denPokemon: {
        38: {name: 'Den 38', link: "https://www.serebii.net/swordshield/maxraidbattles/den38.shtml", gmax: false, swordPokemon: ['714', '840', '782', '885', '714', '840', '886', '715', '783', '784', '841', '887'], shieldPokemon: ['714', '840', '704', '885', '714', '840', '886', '715', '705', '706', '842', '887']},
        64: {name: 'Den 64', link: "https://www.serebii.net/swordshield/maxraidbattles/den64.shtml", gmax: false, swordPokemon: ['328', '840', '610', '782', '885', '611', '783', '776', '784', '886', '612', '887'], shieldPokemon: ['610', '840', '328', '704', '885', '329', '705', '780', '706', '886', '330', '887']},
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
  background-color: #b1cf4b;
}
</style>
