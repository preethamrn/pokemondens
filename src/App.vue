<template>
  <div id="app">
    <div id='wild-area-map'>
      <img alt="Pokemon Wild Area Map" src="./assets/pokemon-wild-area.jpg">
      <DenLocation v-for="(den, index) in dens" :key="index" :position='den.position' :commonDen='denPokemon[den.commonID]' :rareDen='denPokemon[den.rareID]' :gmax='denPokemon[den.commonID].gmax || denPokemon[den.rareID].gmax' :screenshotImg='den.img'/>
    </div>
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
        {commonID: 18, rareID: 77, location: "Lake of Outrage", img: "https://www.serebii.net/swordshield/den/th/lakeofoutrage-3.jpg",  position: {x: 362, y: 215}},
        {commonID: 38, rareID: 64, location: "Axew's Eye", img: "https://www.serebii.net/swordshield/den/th/axew'seye-1.jpg",  position: {x: 572, y: 1456}},
      ],
      denPokemon: {
        18: {name: 'Den 18', link: "https://www.serebii.net/swordshield/maxraidbattles/den18.shtml", gmax: false, swordPokemon: ['037', '850', '757', '607', '554-g', '758', '608', '038', '324', '851', '631', '555-g'], shieldPokemon: ['058', '850', '757', '607', '631', '608', '758', '059', '324', '631', '851', '059']},
        38: {name: 'Den 38', link: "https://www.serebii.net/swordshield/maxraidbattles/den38.shtml", gmax: false, swordPokemon: ['714', '840', '782', '885', '714', '840', '886', '715', '783', '784', '841', '887'], shieldPokemon: ['714', '840', '704', '885', '714', '840', '886', '715', '705', '706', '842', '887']},
        64: {name: 'Den 64', link: "https://www.serebii.net/swordshield/maxraidbattles/den64.shtml", gmax: false, swordPokemon: ['328', '840', '610', '782', '885', '611', '783', '776', '784', '886', '612', '887'], shieldPokemon: ['610', '840', '328', '704', '885', '329', '705', '780', '706', '886', '330', '887']},
        77: {name: 'Den 77', link: "https://www.serebii.net/swordshield/maxraidbattles/den77.shtml", gmax: true, swordPokemon: ['037', '850', '607', '004', '005', '038', '631', '324', '038', '758', '851', '006-gi'], shieldPokemon: ['058', '850', '607', '004', '005', '631', '631', '324', '758', '059', '851', '006-gi']},
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
  padding-bottom: 500px;
}

#wild-area-map {
  position: relative;
  top: 15px;
  left: 10px;
}
</style>
