<template>
  <div class='den' :style="{left: position.x + 'px', top: position.y + 'px'}" @mouseenter="triggerHover()" @mouseleave="clearHover()">
    <img :src="gmax ? '/icons/gmax.png' : '/icons/dmax.png'">
    <v-container v-if='hover && commonDen && rareDen' class='den-hover' fluid>
      <v-row style="justify-content: center;"><img :src='screenshotImg' width="50%"/></v-row>
      <v-row>
        <v-col><den-raid :swordPokemon='commonDen.swordPokemon' :shieldPokemon='commonDen.shieldPokemon' :name='commonDen.name' :link='commonDen.link' type="Common" /></v-col>
        <v-col><den-raid :swordPokemon='rareDen.swordPokemon' :shieldPokemon='rareDen.shieldPokemon' :name='rareDen.name' :link='rareDen.link' type="Rare" /></v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import DenRaid from './DenRaid.vue'

export default {
  name: 'DenLocation',
  components: {
    DenRaid,
  },
  data() {
    return {
      hover: false,
    }
  },
  props: {
    position: Object,
    commonDen: Object,
    rareDen: Object,
    gmax: Boolean,
    screenshotImg: String,
  },
  methods: {
    triggerHover() {
      this.hover = true
    },
    clearHover() {
      this.hover = false
    }
  }
}
</script>

<style scoped>
.den {
  position: absolute;
}
.den-hover {
  background-color: #ffffff;
  position: relative;
  z-index: 100;
}
</style>
