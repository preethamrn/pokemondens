<template>
  <div class='den' :style="{left: position.x + 'px', top: position.y + 'px'}" @mouseenter="triggerHover()" @mouseleave="clearHover">
    <img @touchstart="toggleHover()" :src="!found ? `${publicPath}icons/notfound.png` : gmax ? `${publicPath}icons/gmax.png` : `${publicPath}icons/dmax.png`" :style='{transform: found ? "scale(1.0)" : "scale(0.5)"}'>
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
      publicPath: process.env.VUE_APP_PUBLIC_PATH,
    }
  },
  props: {
    position: Object,
    commonDen: Object,
    rareDen: Object,
    gmax: Boolean,
    screenshotImg: String,
    searchIDs: Array,
  },
  methods: {
    triggerHover() {
      this.hover = true
    },
    clearHover(e) {
      if(e.relatedTarget && e.relatedTarget.tagName == "PINCH-ZOOM") {
        return
      }
      this.hover = false
    },
    toggleHover() {
      this.hover = !this.hover
    }
  },
  computed: {
    found() {
      if (!this.searchIDs || this.searchIDs.length === 0) return true
      if (!this.commonDen || !this.rareDen) return this.searchIDs.length === 0
      for (const i in this.searchIDs) {
        const id = this.searchIDs[i]
        if (this.commonDen.swordPokemon.indexOf(id) >= 0
          || this.rareDen.swordPokemon.indexOf(id) >= 0
          || this.commonDen.shieldPokemon.indexOf(id) >= 0
          || this.rareDen.shieldPokemon.indexOf(id) >= 0) {
            return  true
          }
      }
      return false
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
  overflow: visible;
  width: max-content;
}
</style>
