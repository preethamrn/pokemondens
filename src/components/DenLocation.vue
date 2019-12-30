<template>
  <div class='den' :style="{left: position.x + 'px', top: position.y + 'px'}" @mouseenter="triggerHover()" @mouseleave="clearHover()">
    <img :src="gmax ? gmaxImg : dmaxImg">
    <v-layout v-if='hover'>
      <div class='versions'>
        <div class='sw'>Sword</div>
        <div class='swp pokemon-list'>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
        </div>
        <div class='sh'>Shield</div>
        <div class='shp pokemon-list'>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
          <div class='sprite'></div>
        </div>
      </div>
    </v-layout>
  </div>
</template>

<script>
const dmaxImg = require('../assets/dmax.png')
const gmaxImg = require('../assets/gmax.png')

export default {
  name: 'DenLocation',
  data() {
    return {
      dmaxImg, gmaxImg,
      hover: false,
    }
  },
  props: {
    position: Object,
    pokemon: Array,
    gmax: Boolean,
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
.sh .sw {
  line-height: 100%;
}
.versions {
  position: absolute;
  background-color: #ffffff;
  padding: 10px;
  display: grid;
  grid-template:
    "sw swp" auto
    "sh shp" auto / 1fr 5fr;
}
.pokemon-list {
  display: grid;
  grid: repeat(3, 50px) / auto-flow 60px;
}
.sprite {
  background-color: #8ca0ff;
  width: 47px; height: 47px;
}
</style>
